from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models import Tarea, RegistroTiempo, User
from app.schemas import TareaCreate, TareaUpdate, TareaOut
from app.security import get_db_user

router = APIRouter(prefix="/api/tareas", tags=["tareas"])


def _enrich_tarea(t: Tarea) -> dict:
    minutos = sum(r.minutos for r in t.registros)
    asignado_nombre = t.asignado.nombre if t.asignado else None
    return {
        **{c.name: getattr(t, c.name) for c in t.__table__.columns},
        "minutos_trabajados": minutos,
        "asignado_nombre": asignado_nombre,
    }


@router.get("/", response_model=List[TareaOut])
def listar(proyecto_id: Optional[int] = None, status: Optional[str] = None,
           db: Session = Depends(get_db), _=Depends(get_db_user)):
    q = db.query(Tarea)
    if proyecto_id:
        q = q.filter(Tarea.proyecto_id == proyecto_id)
    if status:
        q = q.filter(Tarea.status == status)
    return [_enrich_tarea(t) for t in q.order_by(Tarea.created_at.desc()).all()]


@router.post("/", response_model=TareaOut)
def crear(data: TareaCreate, db: Session = Depends(get_db), _=Depends(get_db_user)):
    t = Tarea(**data.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return _enrich_tarea(t)


@router.get("/{tid}", response_model=TareaOut)
def detalle(tid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    t = db.query(Tarea).filter_by(id=tid).first()
    if not t:
        raise HTTPException(404, "Tarea no encontrada")
    return _enrich_tarea(t)


@router.patch("/{tid}", response_model=TareaOut)
def editar(tid: int, data: TareaUpdate, db: Session = Depends(get_db),
           _=Depends(get_db_user)):
    t = db.query(Tarea).filter_by(id=tid).first()
    if not t:
        raise HTTPException(404, "Tarea no encontrada")
    updates = data.model_dump(exclude_unset=True)
    if updates.get("status") == "completada" and not t.fecha_fin_real:
        updates["fecha_fin_real"] = date.today()
    for k, v in updates.items():
        setattr(t, k, v)
    db.commit()
    db.refresh(t)
    return _enrich_tarea(t)


@router.delete("/{tid}")
def eliminar(tid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    t = db.query(Tarea).filter_by(id=tid).first()
    if not t:
        raise HTTPException(404, "Tarea no encontrada")
    db.delete(t)
    db.commit()
    return {"ok": True}
