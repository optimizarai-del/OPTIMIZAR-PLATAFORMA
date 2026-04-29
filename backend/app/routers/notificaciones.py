from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Notificacion
from app.schemas import NotificacionOut
from app.security import get_db_user

router = APIRouter(prefix="/api/notificaciones", tags=["notificaciones"])


@router.get("/", response_model=List[NotificacionOut])
def listar(
    limit: int = Query(50, le=200),
    solo_errores: bool = False,
    db: Session = Depends(get_db),
    _=Depends(get_db_user),
):
    q = db.query(Notificacion)
    if solo_errores:
        q = q.filter(Notificacion.enviado == False)
    return q.order_by(Notificacion.created_at.desc()).limit(limit).all()


@router.get("/stats")
def stats(db: Session = Depends(get_db), _=Depends(get_db_user)):
    total   = db.query(Notificacion).count()
    enviadas = db.query(Notificacion).filter(Notificacion.enviado == True).count()
    errores  = db.query(Notificacion).filter(Notificacion.enviado == False).count()
    return {"total": total, "enviadas": enviadas, "errores": errores}
