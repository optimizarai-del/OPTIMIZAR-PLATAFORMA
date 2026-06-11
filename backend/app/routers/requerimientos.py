from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Requerimiento, RequerimientoStatus
from app.schemas import RequerimientoCreate, RequerimientoUpdate, RequerimientoOut
from app.security import get_db_user

router = APIRouter(prefix="/api/requerimientos", tags=["requerimientos"])


@router.get("/", response_model=List[RequerimientoOut])
def listar(status: Optional[RequerimientoStatus] = None, db: Session = Depends(get_db),
           _=Depends(get_db_user)):
    # status tipado con el enum: FastAPI valida y responde 422 si llega un valor inválido
    q = db.query(Requerimiento)
    if status:
        q = q.filter(Requerimiento.status == status)
    return q.order_by(Requerimiento.created_at.desc()).all()


@router.post("/", response_model=RequerimientoOut)
def crear(data: RequerimientoCreate, db: Session = Depends(get_db),
          _=Depends(get_db_user)):
    req = Requerimiento(**data.model_dump())
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


@router.get("/{rid}", response_model=RequerimientoOut)
def detalle(rid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    req = db.query(Requerimiento).filter_by(id=rid).first()
    if not req:
        raise HTTPException(404, "Requerimiento no encontrado")
    return req


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
    return req


@router.delete("/{rid}")
def eliminar(rid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    req = db.query(Requerimiento).filter_by(id=rid).first()
    if not req:
        raise HTTPException(404, "Requerimiento no encontrado")
    db.delete(req)
    db.commit()
    return {"ok": True}
