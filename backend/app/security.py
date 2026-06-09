from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.orm import Session
import os

SECRET_KEY = os.getenv("SECRET_KEY", "optimizar-secret-key-change-in-production-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10080))

# Clave para el endpoint externo del CRM (integraciones: n8n, webhooks, scripts).
EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY", "")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(key: str = Depends(api_key_header)):
    """Protege el endpoint externo del CRM. Compara contra EXTERNAL_API_KEY del .env.
    Si la clave no está configurada, el endpoint queda deshabilitado (503)."""
    if not EXTERNAL_API_KEY:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE,
                            "Endpoint externo deshabilitado: EXTERNAL_API_KEY no configurada.")
    if not key or key != EXTERNAL_API_KEY:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "API Key inválida o ausente.",
                            headers={"WWW-Authenticate": "X-API-Key"})
    return True


def hash_pw(p: str) -> str:
    return pwd_context.hash(p)


def verify_pw(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2), db: Session = Depends(lambda: None)):
    from app.models import User
    from app.database import get_db
    cred_exc = HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas",
                             headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise cred_exc
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == uid).first()
    finally:
        db.close()
    if not user:
        raise cred_exc
    return user


def get_db_user(token: str = Depends(oauth2)):
    from app.models import User
    from app.database import SessionLocal
    cred_exc = HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas",
                             headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise cred_exc
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == uid).first()
        if not user:
            raise cred_exc
        return user
    finally:
        db.close()
