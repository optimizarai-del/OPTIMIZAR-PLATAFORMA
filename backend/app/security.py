from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.orm import Session
import logging
import os
import secrets
from pathlib import Path

logger = logging.getLogger("optimizar.security")


def _load_secret_key() -> str:
    """Resuelve la SECRET_KEY para firmar JWT.
    1) Si existe la env var SECRET_KEY, se usa esa.
    2) Si no, se usa/genera una clave aleatoria persistida en backend/.secret_key
       (ignorada por git), para que los tokens sobrevivan reinicios.
    Nunca usa un default hardcodeado."""
    env_key = os.getenv("SECRET_KEY")
    if env_key:
        return env_key

    key_file = Path(__file__).resolve().parents[1] / ".secret_key"
    try:
        if key_file.exists():
            key = key_file.read_text(encoding="utf-8").strip()
            if key:
                logger.warning(
                    "SECRET_KEY no configurada en el entorno; usando clave persistida en %s. "
                    "Configurá SECRET_KEY en el .env para producción.", key_file)
                return key
        key = secrets.token_urlsafe(64)
        key_file.write_text(key, encoding="utf-8")
        logger.warning(
            "SECRET_KEY no configurada en el entorno; se generó una clave aleatoria y se "
            "persistió en %s. Configurá SECRET_KEY en el .env para producción.", key_file)
        return key
    except OSError as e:
        # No se pudo persistir: clave efímera (los JWT se invalidan al reiniciar).
        logger.warning(
            "SECRET_KEY no configurada y no se pudo persistir %s (%s). "
            "Usando clave efímera: los tokens se invalidarán al reiniciar.", key_file, e)
        return secrets.token_urlsafe(64)


SECRET_KEY = _load_secret_key()
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
    if not key or not secrets.compare_digest(key, EXTERNAL_API_KEY):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "API Key inválida o ausente.",
                            headers={"WWW-Authenticate": "X-API-Key"})
    return True


def hash_pw(p: str) -> str:
    return pwd_context.hash(p)


def verify_pw(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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


def require_manager(token: str = Depends(oauth2)):
    """Dependencia: exige rol admin o manager. Reusá esto en endpoints sensibles."""
    from app.models import UserRole
    user = get_db_user(token)
    if user.role not in (UserRole.admin, UserRole.manager):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Sin permisos")
    return user


def require_editor(token: str = Depends(oauth2)):
    """Dependencia: permite escribir a todos menos `viewer` (read-only)."""
    from app.models import UserRole
    user = get_db_user(token)
    if user.role == UserRole.viewer:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo lectura")
    return user
