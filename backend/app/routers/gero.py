"""Router de Gero — el asistente IA de OPTIMIZAR en WhatsApp.

- POST /api/gero/mensaje  : ENTRADA PRINCIPAL desde n8n. Recibe el mensaje ya normalizado
                            (texto / audio transcripto / imagen descripta), piensa la respuesta
                            y la DEVUELVE en el body para que n8n la mande por WhatsApp. (X-API-Key)
- POST /api/gero/webhook  : alternativa — recibe el webhook crudo de YCloud y envía él mismo (token).
- GET  /api/gero/webhook  : verificación/health del webhook.
- POST /api/gero/test     : simula un mensaje para probar el cerebro (JWT, sin tocar WhatsApp).
- GET  /api/gero/conversaciones[/{id}] : observabilidad para el equipo (JWT).
"""
import re
import logging
from typing import Optional, List

from fastapi import (APIRouter, Depends, BackgroundTasks, Request, Query,
                     Header, HTTPException)
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
from app.models import GeroConversacion, GeroMensaje
from app.security import get_db_user, require_manager, verify_api_key
from app.gero import cerebro
from app.gero.ycloud import parse_inbound, es_evento_entrante, webhook_autorizado, enviar_whatsapp

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/gero", tags=["gero"])


def _solo_digitos(s: str) -> str:
    """Convierte un teléfono ('+5492954407096') al wa_id de WhatsApp ('5492954407096')."""
    return re.sub(r"\D", "", s or "")


# ── ENTRADA PRINCIPAL: n8n → Gero → (respuesta) → n8n → WhatsApp ──────────────

class GeroMensajeIn(BaseModel):
    """Payload que manda el flujo de n8n al final de su preprocesamiento.
    `mensaje` ya viene normalizado a texto (transcripción de audio o descripción de imagen incluidas)."""
    telefono: str                       # el 'from' de YCloud, ej "+5492954407096"
    mensaje: str                        # texto ya normalizado por n8n
    nombre: Optional[str] = None        # customerProfile.name
    wa_message_id: Optional[str] = None # wamid, para idempotencia (opcional)


@router.post("/mensaje", tags=["gero-external"])
def recibir_mensaje(data: GeroMensajeIn, db: Session = Depends(get_db),
                    _=Depends(verify_api_key)):
    """Recibe un mensaje ya procesado por n8n, corre el cerebro de Gero (memoria + tools del CRM)
    y DEVUELVE la respuesta para que n8n la envíe por WhatsApp.

    Respuesta:
      { "respuesta": "<texto de Gero o null>", "enviar": <bool>,
        "conversacion_id": int, "estado": str, "nivel_interes": str|null }
    `enviar=false` cuando no hay que responder (duplicado, conversación en handoff humano, o error)."""
    wa_id = _solo_digitos(data.telefono)
    if not wa_id or not (data.mensaje or "").strip():
        raise HTTPException(422, "Faltan 'telefono' o 'mensaje'.")

    respuesta = cerebro.responder(
        db, wa_id=wa_id, texto=data.mensaje.strip(),
        telefono=data.telefono, nombre=data.nombre, wa_message_id=data.wa_message_id,
    )
    conv = db.query(GeroConversacion).filter_by(wa_id=wa_id).first()
    return {
        "respuesta": respuesta,
        "enviar": bool(respuesta),
        "conversacion_id": conv.id if conv else None,
        "estado": conv.estado if conv else None,
        "nivel_interes": conv.nivel_interes if conv else None,
    }


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
