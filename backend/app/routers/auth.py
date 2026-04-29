from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserRole
from app.schemas import LoginRequest, TokenResponse, UserCreate, UserOut
from app.security import hash_pw, verify_pw, create_token, get_db_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_pw(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas")
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Usuario inactivo")
    token = create_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.post("/register", response_model=TokenResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email ya registrado")
    is_first = db.query(User).count() == 0
    role = UserRole.admin if is_first else data.role
    user = User(
        nombre=data.nombre,
        email=data.email,
        password_hash=hash_pw(data.password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_db_user)):
    return current_user
