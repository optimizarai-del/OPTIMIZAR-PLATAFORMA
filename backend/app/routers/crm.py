from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import (Oportunidad, EtapaOportunidad, FuenteOportunidad,
                        Proyecto, ProyectoStatus, User, UserRole)
from app.schemas import (OportunidadCreate, OportunidadUpdate, OportunidadOut,
                         OportunidadExternal, CRMStats, ProyectoOut)
from app.security import get_db_user, verify_api_key

router = APIRouter(prefix="/api/crm", tags=["crm"])

ETAPAS_ABIERTAS = [EtapaOportunidad.lead, EtapaOportunidad.contactado,
                   EtapaOportunidad.propuesta, EtapaOportunidad.negociacion]


# ── CRUD (autenticado con JWT) ────────────────────────────────────────────────

@router.get("/oportunidades", response_model=List[OportunidadOut])
def listar(db: Session = Depends(get_db), _=Depends(get_db_user)):
    return (db.query(Oportunidad)
              .order_by(Oportunidad.etapa, Oportunidad.orden, Oportunidad.created_at.desc())
              .all())


@router.post("/oportunidades", response_model=OportunidadOut)
def crear(data: OportunidadCreate, db: Session = Depends(get_db), _=Depends(get_db_user)):
    # nueva oportunidad va al fondo de su columna
    base = db.query(Oportunidad).filter_by(etapa=data.etapa).count()
    op = Oportunidad(**data.model_dump(), orden=base)
    db.add(op)
    db.commit()
    db.refresh(op)
    return op


@router.get("/oportunidades/{oid}", response_model=OportunidadOut)
def detalle(oid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    op = db.query(Oportunidad).filter_by(id=oid).first()
    if not op:
        raise HTTPException(404, "Oportunidad no encontrada")
    return op


@router.patch("/oportunidades/{oid}", response_model=OportunidadOut)
def editar(oid: int, data: OportunidadUpdate, db: Session = Depends(get_db),
           _=Depends(get_db_user)):
    op = db.query(Oportunidad).filter_by(id=oid).first()
    if not op:
        raise HTTPException(404, "Oportunidad no encontrada")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(op, k, v)
    db.commit()
    db.refresh(op)
    return op


@router.delete("/oportunidades/{oid}")
def eliminar(oid: int, db: Session = Depends(get_db),
             current_user: User = Depends(get_db_user)):
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(403, "Sin permisos")
    op = db.query(Oportunidad).filter_by(id=oid).first()
    if not op:
        raise HTTPException(404, "Oportunidad no encontrada")
    db.delete(op)
    db.commit()
    return {"ok": True}


@router.post("/oportunidades/{oid}/convertir", response_model=ProyectoOut)
def convertir_a_proyecto(oid: int, db: Session = Depends(get_db),
                         current_user: User = Depends(get_db_user)):
    """Convierte una oportunidad ganada en un Proyecto y las deja vinculadas."""
    op = db.query(Oportunidad).filter_by(id=oid).first()
    if not op:
        raise HTTPException(404, "Oportunidad no encontrada")
    if op.proyecto_id:
        raise HTTPException(400, "La oportunidad ya está vinculada a un proyecto.")

    p = Proyecto(
        nombre=op.titulo,
        cliente=op.empresa,
        descripcion=op.descripcion,
        status=ProyectoStatus.planificacion,
        created_by=current_user.id,
    )
    db.add(p)
    db.flush()                       # obtener p.id sin segundo commit
    op.proyecto_id = p.id
    op.etapa = EtapaOportunidad.ganado
    db.commit()
    db.refresh(p)
    # _enrich vive en proyectos.py; acá devolvemos los campos calculados en cero
    return {
        **p.__dict__,
        "progreso": 0.0, "total_tareas": 0, "tareas_completadas": 0,
        "total_puntos": 0, "puntos_completados": 0,
    }


@router.get("/stats", response_model=CRMStats)
def stats(db: Session = Depends(get_db), _=Depends(get_db_user)):
    ops = db.query(Oportunidad).all()
    por_etapa = {e.value: {"count": 0, "valor": 0.0} for e in EtapaOportunidad}
    valor_pipeline = valor_ganado = 0.0
    ganadas = perdidas = 0
    for op in ops:
        cell = por_etapa[op.etapa.value]
        cell["count"] += 1
        cell["valor"] += op.valor_estimado or 0.0
        if op.etapa in ETAPAS_ABIERTAS:
            valor_pipeline += op.valor_estimado or 0.0
        elif op.etapa == EtapaOportunidad.ganado:
            valor_ganado += op.valor_estimado or 0.0
            ganadas += 1
        elif op.etapa == EtapaOportunidad.perdido:
            perdidas += 1
    return CRMStats(
        total_oportunidades=len(ops),
        valor_pipeline=round(valor_pipeline, 2),
        valor_ganado=round(valor_ganado, 2),
        ganadas=ganadas,
        perdidas=perdidas,
        por_etapa=por_etapa,
    )


# ── Endpoint EXTERNO (API Key) ────────────────────────────────────────────────
# Permite a sistemas externos (n8n, formularios web, scripts) crear o actualizar
# oportunidades de forma idempotente usando `external_id`.

@router.post("/external/oportunidades", response_model=OportunidadOut,
             tags=["crm-external"])
def upsert_externo(data: OportunidadExternal, db: Session = Depends(get_db),
                   _=Depends(verify_api_key)):
    op = db.query(Oportunidad).filter_by(external_id=data.external_id).first()
    payload = data.model_dump(exclude_unset=True)

    if op:                                   # UPDATE
        for k, v in payload.items():
            setattr(op, k, v)
    else:                                    # CREATE
        etapa = payload.pop("etapa", None) or EtapaOportunidad.lead
        base = db.query(Oportunidad).filter_by(etapa=etapa).count()
        op = Oportunidad(
            titulo=payload.pop("titulo", None) or payload["empresa"],
            etapa=etapa,
            fuente=FuenteOportunidad.api,
            orden=base,
            **payload,
        )
        db.add(op)
    db.commit()
    db.refresh(op)
    return op
