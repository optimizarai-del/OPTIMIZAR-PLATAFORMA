from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models import (Oportunidad, EtapaOportunidad, FuenteOportunidad,
                        Proyecto, ProyectoStatus, User, UserRole,
                        LeadJob, ChatMensaje)
from app.schemas import (OportunidadCreate, OportunidadUpdate, OportunidadOut,
                         OportunidadExternal, CRMStats, ProyectoOut,
                         LeadJobCreate, LeadJobUpdate, LeadJobOut,
                         ChatMensajeCreate, ChatMensajeOut, FunnelNotify,
                         RespuestaInbound)
from app.security import get_db_user, verify_api_key

router = APIRouter(prefix="/api/crm", tags=["crm"])

ETAPAS_ABIERTAS = [EtapaOportunidad.lead, EtapaOportunidad.contactado,
                   EtapaOportunidad.propuesta, EtapaOportunidad.negociacion]

# Campos que nunca se actualizan desde el payload (anti mass-assignment).
CAMPOS_PROHIBIDOS = {"id", "created_by", "created_at", "updated_at", "user_id",
                     "external_id", "fuente"}


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
        if k in CAMPOS_PROHIBIDOS:
            continue
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
            if k in CAMPOS_PROHIBIDOS:       # external_id ya coincide; no se reescribe
                continue
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


# ── Disparo manual del outreach en código (envío / escucha) ───────────────────
# Útil para testear sin esperar al scheduler. Protegidos con JWT (uso interno).

@router.post("/outreach/enviar")
def disparar_envio(db: Session = Depends(get_db), current_user: User = Depends(get_db_user)):
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(403, "Sin permisos")
    from app.outreach_service import enviar_pendientes
    enviados = enviar_pendientes(db)
    return {"enviados": enviados}


@router.post("/outreach/revisar-inbox")
def disparar_inbox(db: Session = Depends(get_db), current_user: User = Depends(get_db_user)):
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(403, "Sin permisos")
    from app.outreach_service import revisar_inbox
    registradas = revisar_inbox(db)
    return {"registradas": registradas}


@router.get("/external/outbox", response_model=List[OportunidadOut], tags=["crm-external"])
def outbox(db: Session = Depends(get_db), _=Depends(verify_api_key)):
    """Leads con email YA escrito y pendientes de envío. Lo consume n8n para disparar
    los correos. Devuelve solo los que tienen contacto_email y outreach_status='escrito'."""
    return (db.query(Oportunidad)
              .filter(Oportunidad.outreach_status == "escrito",
                      Oportunidad.contacto_email.isnot(None))
              .order_by(Oportunidad.created_at)
              .all())


@router.post("/external/respuesta", tags=["crm-external"])
def registrar_respuesta(data: RespuestaInbound, db: Session = Depends(get_db),
                        _=Depends(verify_api_key)):
    """Registra la respuesta de un lead (la trae n8n desde el inbox). Matchea la
    oportunidad por contacto_email (la más reciente), marca outreach_status='respondido',
    guarda el texto y mueve la etapa a 'contactado' si todavía estaba en 'lead'."""
    op = (db.query(Oportunidad)
            .filter(Oportunidad.contacto_email == data.email)
            .order_by(Oportunidad.created_at.desc())
            .first())
    if not op:
        return {"matched": False}
    op.respuesta_recibida = data.texto
    op.outreach_status = "respondido"
    if op.etapa == EtapaOportunidad.lead:
        op.etapa = EtapaOportunidad.contactado
    db.commit()
    return {"matched": True, "id": op.id, "empresa": op.empresa}


# ── Cola de búsqueda (Lead Jobs) ──────────────────────────────────────────────
# La plataforma encola pedidos (JWT); el Equipo de Venta y Prospección los
# consume por polling (API Key) y devuelve los leads vía /external/oportunidades.

@router.post("/lead-jobs", response_model=LeadJobOut)
def crear_lead_job(data: LeadJobCreate, db: Session = Depends(get_db),
                   _=Depends(get_db_user)):
    job = LeadJob(icp=data.icp, cantidad=data.cantidad, fundamento=data.fundamento)
    db.add(job); db.commit(); db.refresh(job)
    return job


@router.get("/lead-jobs", response_model=List[LeadJobOut])
def listar_lead_jobs(db: Session = Depends(get_db), _=Depends(get_db_user)):
    return db.query(LeadJob).order_by(LeadJob.created_at.desc()).all()


@router.get("/lead-jobs/pending", response_model=List[LeadJobOut], tags=["crm-external"])
def lead_jobs_pendientes(db: Session = Depends(get_db), _=Depends(verify_api_key)):
    return (db.query(LeadJob).filter_by(status="pendiente")
              .order_by(LeadJob.created_at).all())


@router.patch("/lead-jobs/{jid}", response_model=LeadJobOut, tags=["crm-external"])
def actualizar_lead_job(jid: int, data: LeadJobUpdate, db: Session = Depends(get_db),
                        _=Depends(verify_api_key)):
    job = db.query(LeadJob).filter_by(id=jid).first()
    if not job:
        raise HTTPException(404, "Lead job no encontrado")
    if data.status is not None:
        job.status = data.status
        if data.status in ("completado", "error"):
            job.processed_at = datetime.utcnow()
    if data.resumen is not None:
        job.resumen = data.resumen
    db.commit(); db.refresh(job)
    return job


# ── Chat persistente (humano ↔ orquestador) ───────────────────────────────────

@router.get("/chat", response_model=List[ChatMensajeOut])
def listar_chat(db: Session = Depends(get_db), _=Depends(get_db_user)):
    return db.query(ChatMensaje).order_by(ChatMensaje.created_at).all()


@router.post("/chat", response_model=ChatMensajeOut)
def postear_humano(data: ChatMensajeCreate, db: Session = Depends(get_db),
                   _=Depends(get_db_user)):
    msg = ChatMensaje(rol="humano", contenido=data.contenido)
    db.add(msg); db.commit(); db.refresh(msg)
    return msg


@router.patch("/chat/{mid}/estado", response_model=ChatMensajeOut)
def set_estado_chat(mid: int, estado: str, db: Session = Depends(get_db),
                    _=Depends(get_db_user)):
    """El humano aprueba/rechaza una acción propuesta por el agente."""
    msg = db.query(ChatMensaje).filter_by(id=mid).first()
    if not msg:
        raise HTTPException(404, "Mensaje no encontrado")
    msg.estado = estado                      # aprobado / rechazado
    db.commit(); db.refresh(msg)
    return msg


@router.post("/external/chat", response_model=ChatMensajeOut, tags=["crm-external"])
def postear_agente(data: ChatMensajeCreate, db: Session = Depends(get_db),
                   _=Depends(verify_api_key)):
    msg = ChatMensaje(
        rol="agente",
        contenido=data.contenido,
        requiere_aprobacion=data.requiere_aprobacion,
        estado="esperando" if data.requiere_aprobacion else "info",
    )
    db.add(msg); db.commit(); db.refresh(msg)
    return msg


# ── Aviso por mail a los dos correos del funnel ───────────────────────────────

@router.post("/external/notify", tags=["crm-external"])
def notificar_funnel(data: FunnelNotify, _=Depends(verify_api_key)):
    from app.email_service import enviar_aviso_funnel
    res = enviar_aviso_funnel(
        asunto=data.asunto, titulo=data.titulo,
        subtitulo=data.subtitulo or "", cuerpo_html=data.cuerpo,
        prioridad=data.prioridad or "info",
    )
    return {
        "enviados": [e for e, err in res.items() if err is None],
        "fallidos": {e: err for e, err in res.items() if err is not None},
    }
