from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Servicio
from app.schemas import ServicioCreate, ServicioUpdate, ServicioOut
from app.security import get_db_user

router = APIRouter(prefix="/api/servicios", tags=["servicios"])


@router.get("/", response_model=List[ServicioOut])
def listar(solo_activos: Optional[bool] = None, db: Session = Depends(get_db),
           _=Depends(get_db_user)):
    q = db.query(Servicio)
    if solo_activos:
        q = q.filter(Servicio.activo.is_(True))
    return q.order_by(Servicio.nombre.asc()).all()


@router.post("/", response_model=ServicioOut)
def crear(data: ServicioCreate, db: Session = Depends(get_db), _=Depends(get_db_user)):
    serv = Servicio(**data.model_dump())
    db.add(serv)
    db.commit()
    db.refresh(serv)
    return serv


@router.patch("/{sid}", response_model=ServicioOut)
def editar(sid: int, data: ServicioUpdate, db: Session = Depends(get_db),
           _=Depends(get_db_user)):
    serv = db.query(Servicio).filter_by(id=sid).first()
    if not serv:
        raise HTTPException(404, "Servicio no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(serv, k, v)
    db.commit()
    db.refresh(serv)
    return serv


@router.delete("/{sid}")
def eliminar(sid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    serv = db.query(Servicio).filter_by(id=sid).first()
    if not serv:
        raise HTTPException(404, "Servicio no encontrado")
    db.delete(serv)
    db.commit()
    return {"ok": True}
