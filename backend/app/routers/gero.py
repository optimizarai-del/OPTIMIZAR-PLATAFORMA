"""Router de Gero — el asistente IA de OPTIMIZAR en WhatsApp.

- POST /api/gero/webhook  : recibe los mensajes entrantes de YCloud (público, protegido por token).
- GET  /api/gero/webhook  : verificación/health del webhook.
- POST /api/gero/test     : simula un mensaje para probar el cerebro (JWT, sin tocar WhatsApp).
- GET  /api/gero/conversaciones[/{id}] : observabilidad para el equipo (JWT).
"""
import logging
from typing import Optional, List

from fastapi import (APIRouter, Depends, BackgroundTasks, Request, Query,
                     Header, HTTPException)
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
from app.models import GeroConversacion, GeroMensaje
from app.security import get_db_user, require_manager
from app.gero import cerebro
from app.gero.ycloud import parse_inbound, es_evento_entrante, webhook_autorizado, enviar_whatsapp

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/gero", tags=["gero"])


# ── Procesamiento en background (para responder rápido al webhook) ────────────

def _procesar_y_responder(payload: dict) -> None:
    """Corre fuera del request: piensa la respuesta y la manda por WhatsApp.
    Usa su propia sesión de DB (la del request ya se cerró)."""
    data = parse_inbound(payload)
    if not data:
        return
    db = SessionLocal()
    try:
        respuesta = cerebro.responder(
            db,
            wa_id=data["wa_id"],
            texto=data["texto"],
            telefono=data.get("telefono"),
            nombre=data.get("nombre"),
            wa_message_id=data.get("wa_message_id"),
        )
        if respuesta:
            enviar_whatsapp(data["telefono"], respuesta)
    except Exception as e:  # nunca dejamos que un error tumbe el worker
        logger.exception("[gero] error procesando inbound: %s", e)
    finally:
        db.close()


# ── Webhook de YCloud ─────────────────────────────────────────────────────────

@router.get("/webhook")
def webhook_verify():
    """Health/verificación del webhook (YCloud o un chequeo manual)."""
    return {"ok": True, "agente": "gero"}


@router.post("/webhook")
async def webhook(request: Request, bg: BackgroundTasks,
                  token: Optional[str] = Query(None),
                  x_webhook_token: Optional[str] = Header(None, alias="X-Webhook-Token")):
    """Recibe eventos de YCloud. Responde 200 al toque y procesa en background."""
    if not webhook_autorizado(x_webhook_token or token):
        raise HTTPException(401, "Webhook no autorizado")
    try:
        payload = await request.json()
    except Exception:
        return {"ok": True, "ignored": "body no-JSON"}

    if es_evento_entrante(payload):
        bg.add_task(_procesar_y_responder, payload)
        return {"ok": True, "procesando": True}
    return {"ok": True, "procesando": False}


# ── Prueba del cerebro (sin WhatsApp) ─────────────────────────────────────────

class GeroTestIn(BaseModel):
    wa_id: str = "test-000"
    texto: str
    nombre: Optional[str] = None


@router.post("/test")
def probar(data: GeroTestIn, db: Session = Depends(get_db), _=Depends(require_manager)):
    """Simula un mensaje entrante y devuelve la respuesta de Gero SIN mandar nada a WhatsApp.
    Ideal para probar personalidad, memoria y herramientas del CRM."""
    respuesta = cerebro.responder(
        db, wa_id=data.wa_id, texto=data.texto,
        telefono=f"+{data.wa_id}", nombre=data.nombre, wa_message_id=None,
    )
    return {"respuesta": respuesta}


# ── Observabilidad (para el equipo / futuro panel) ────────────────────────────

@router.get("/conversaciones")
def listar_conversaciones(db: Session = Depends(get_db), _=Depends(get_db_user)):
    convs = (db.query(GeroConversacion)
               .order_by(GeroConversacion.ultima_actividad.desc())
               .all())
    return [{
        "id": c.id,
        "wa_id": c.wa_id,
        "telefono": c.telefono,
        "nombre": c.nombre_perfil,
        "estado": c.estado,
        "nivel_interes": c.nivel_interes,
        "contacto_id": c.contacto_id,
        "ultima_actividad": c.ultima_actividad,
        "mensajes": len(c.mensajes),
    } for c in convs]


@router.get("/conversaciones/{cid}")
def detalle_conversacion(cid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    c = db.query(GeroConversacion).filter_by(id=cid).first()
    if not c:
        raise HTTPException(404, "Conversación no encontrada")
    return {
        "id": c.id,
        "wa_id": c.wa_id,
        "telefono": c.telefono,
        "nombre": c.nombre_perfil,
        "estado": c.estado,
        "nivel_interes": c.nivel_interes,
        "contacto_id": c.contacto_id,
        "resumen": c.resumen,
        "mensajes": [{
            "rol": m.rol,
            "contenido": m.contenido,
            "herramientas": m.herramientas,
            "created_at": m.created_at,
        } for m in c.mensajes],
    }
