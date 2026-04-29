from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import RegistroTiempo, Tarea, User
from app.schemas import RegistroTiempoCreate, RegistroTiempoOut
from app.security import get_db_user

router = APIRouter(prefix="/api/tiempo", tags=["tiempo"])


def _enrich(r: RegistroTiempo) -> dict:
    return {
        **{c.name: getattr(r, c.name) for c in r.__table__.columns},
        "user_nombre": r.user.nombre if r.user else None,
    }


@router.get("/", response_model=List[RegistroTiempoOut])
def listar(tarea_id: Optional[int] = None, db: Session = Depends(get_db),
           _=Depends(get_db_user)):
    q = db.query(RegistroTiempo)
    if tarea_id:
        q = q.filter(RegistroTiempo.tarea_id == tarea_id)
    return [_enrich(r) for r in q.order_by(RegistroTiempo.fecha.desc()).all()]


@router.post("/", response_model=RegistroTiempoOut)
def registrar(data: RegistroTiempoCreate, db: Session = Depends(get_db),
              current_user: User = Depends(get_db_user)):
    tarea = db.query(Tarea).filter_by(id=data.tarea_id).first()
    if not tarea:
        raise HTTPException(404, "Tarea no encontrada")
    if data.minutos <= 0:
        raise HTTPException(400, "Los minutos deben ser mayores a 0")
    r = RegistroTiempo(**data.model_dump(), user_id=current_user.id)
    db.add(r)
    db.commit()
    db.refresh(r)
    return _enrich(r)


@router.delete("/{rid}")
def eliminar(rid: int, db: Session = Depends(get_db),
             current_user: User = Depends(get_db_user)):
    r = db.query(RegistroTiempo).filter_by(id=rid).first()
    if not r:
        raise HTTPException(404, "Registro no encontrado")
    if r.user_id != current_user.id:
        raise HTTPException(403, "Solo podés eliminar tus propios registros")
    db.delete(r)
    db.commit()
    return {"ok": True}
