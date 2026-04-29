from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, UserRole
from app.schemas import UserOut, UserUpdate
from app.security import get_db_user

router = APIRouter(prefix="/api/users", tags=["users"])


def require_admin(current_user: User = Depends(get_db_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(403, "Se requiere rol admin")
    return current_user


@router.get("/", response_model=List[UserOut])
def listar(db: Session = Depends(get_db), _=Depends(get_db_user)):
    return db.query(User).all()


@router.patch("/{uid}", response_model=UserOut)
def editar(uid: int, data: UserUpdate, db: Session = Depends(get_db),
           current_user: User = Depends(require_admin)):
    user = db.query(User).filter_by(id=uid).first()
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{uid}")
def eliminar(uid: int, db: Session = Depends(get_db),
             current_user: User = Depends(require_admin)):
    user = db.query(User).filter_by(id=uid).first()
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    if user.id == current_user.id:
        raise HTTPException(400, "No podés eliminarte a vos mismo")
    db.delete(user)
    db.commit()
    return {"ok": True}
