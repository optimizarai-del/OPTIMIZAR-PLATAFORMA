from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from app.database import get_db
from app.models import Requerimiento, RequerimientoStatus, Servicio, AnalisisEstado
from app.schemas import RequerimientoCreate, RequerimientoUpdate, RequerimientoOut
from app.security import get_db_user
from app import ai_service

router = APIRouter(prefix="/api/requerimientos", tags=["requerimientos"])


def _serialize(req: Requerimiento) -> RequerimientoOut:
    """Completa servicio_match_nombre para la UI sin exponer la relación entera."""
    out = RequerimientoOut.model_validate(req)
    out.servicio_match_nombre = req.servicio_match.nombre if req.servicio_match else None
    return out


def _analizar_requerimiento(req: Requerimiento, db: Session) -> None:
    """Corre el análisis IA del requerimiento contra el catálogo de servicios y
    persiste el resultado. Nunca levanta: ante un fallo deja estado='error'."""
    try:
        servicios = db.query(Servicio).filter(Servicio.activo.is_(True)).all()
        servicios_dicts = [{
            "id": s.id, "nombre": s.nombre, "categoria": s.categoria,
            "descripcion": s.descripcion, "capacidades": s.capacidades,
        } for s in servicios]
        req_dict = {
            "nombre_cliente": req.nombre_cliente, "sector": req.sector,
            "nombre_proceso": req.nombre_proceso, "trigger_proceso": req.trigger_proceso,
            "pasos_manuales": req.pasos_manuales, "sistemas_core": req.sistemas_core,
            "uso_ia": req.uso_ia,
        }
        res = ai_service.match_requerimiento_servicios(req_dict, servicios_dicts)

        req.analisis_estado = (
            AnalisisEstado.cubierto.value if res.get("cubierto")
            else AnalisisEstado.no_cubierto.value
        )
        req.servicio_match_id = res.get("servicio_id") if res.get("cubierto") else None
        req.analisis_justificacion = res.get("justificacion")
        req.analisis_confianza = res.get("confianza")
    except Exception as e:
        req.analisis_estado = AnalisisEstado.error.value
        req.analisis_justificacion = f"No se pudo completar el análisis: {e}"
        req.servicio_match_id = None
    finally:
        req.analisis_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(req)


@router.get("/", response_model=List[RequerimientoOut])
def listar(status: Optional[RequerimientoStatus] = None, db: Session = Depends(get_db),
           _=Depends(get_db_user)):
    q = db.query(Requerimiento)
    if status:
        q = q.filter(Requerimiento.status == status)
    reqs = q.order_by(Requerimiento.created_at.desc()).all()
    return [_serialize(r) for r in reqs]


@router.post("/", response_model=RequerimientoOut)
def crear(data: RequerimientoCreate, db: Session = Depends(get_db),
          _=Depends(get_db_user)):
    req = Requerimiento(**data.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)
    # Análisis automático apenas se carga el requerimiento.
    _analizar_requerimiento(req, db)
    return _serialize(req)


@router.get("/{rid}", response_model=RequerimientoOut)
def detalle(rid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    req = db.query(Requerimiento).filter_by(id=rid).first()
    if not req:
        raise HTTPException(404, "Requerimiento no encontrado")
    return _serialize(req)


@router.post("/{rid}/analizar", response_model=RequerimientoOut)
def reanalizar(rid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    """Re-corre el análisis manualmente (ej: tras editar el catálogo de servicios)."""
    req = db.query(Requerimiento).filter_by(id=rid).first()
    if not req:
        raise HTTPException(404, "Requerimiento no encontrado")
    _analizar_requerimiento(req, db)
    return _serialize(req)


@router.patch("/{rid}", response_model=RequerimientoOut)
def editar(rid: int, data: RequerimientoUpdate, db: Session = Depends(get_db),
           _=Depends(get_db_user)):
    req = db.query(Requerimiento).filter_by(id=rid).first()
    if not req:
        raise HTTPException(404, "Requerimiento no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(req, k, v)
    db.commit()
    db.refresh(req)
    return _serialize(req)


@router.delete("/{rid}")
def eliminar(rid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    req = db.query(Requerimiento).filter_by(id=rid).first()
    if not req:
        raise HTTPException(404, "Requerimiento no encontrado")
    db.delete(req)
    db.commit()
    return {"ok": True}
