"""Transporte de WhatsApp vía YCloud (https://ycloud.com).

- `enviar_whatsapp`  : manda un mensaje de texto por la API de YCloud (httpx, igual patrón que ai_service).
- `parse_inbound`    : normaliza el payload del webhook de YCloud a un dict simple.
- `webhook_autorizado`: chequeo de seguridad del webhook (token compartido).

Config por env:
  YCLOUD_API_KEY        API key de YCloud (header X-API-Key).
  GERO_PHONE_NUMBER     número de WhatsApp Business desde el que responde Gero (E.164, ej. 549341...).
  YCLOUD_WEBHOOK_SECRET token compartido para validar el webhook (opcional pero MUY recomendado).
"""
import os
import hmac
import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

YCLOUD_API_URL = "https://api.ycloud.com/v2/whatsapp/messages"


def _api_key() -> str:
    return os.getenv("YCLOUD_API_KEY", "").strip()


def _from_number() -> str:
    return os.getenv("GERO_PHONE_NUMBER", "").strip()


def enviar_whatsapp(to: str, texto: str) -> tuple[bool, Optional[str]]:
    """Envía un mensaje de texto por WhatsApp a `to` (número E.164, con o sin '+').
    Devuelve (ok, error). No levanta excepciones."""
    api_key = _api_key()
    desde = _from_number()
    faltan = [n for n, v in [("YCLOUD_API_KEY", api_key), ("GERO_PHONE_NUMBER", desde)] if not v]
    if faltan:
        msg = f"YCloud sin configurar, faltan env: {faltan}"
        logger.warning("[gero] %s", msg)
        return False, msg

    destino = to.lstrip("+")
    try:
        r = httpx.post(
            YCLOUD_API_URL,
            headers={"X-API-Key": api_key, "Content-Type": "application/json"},
            json={
                "from": desde,
                "to": destino,
                "type": "text",
                "text": {"body": texto[:4096]},  # límite de WhatsApp
            },
            timeout=30,
        )
        r.raise_for_status()
        logger.info("[gero] mensaje enviado a %s (HTTP %s)", destino, r.status_code)
        return True, None
    except httpx.HTTPStatusError as e:
        err = f"YCloud {e.response.status_code}: {e.response.text[:300]}"
        logger.warning("[gero] envío falló: %s", err)
        return False, err
    except Exception as e:
        logger.warning("[gero] envío excepción: %s", e)
        return False, str(e)


def _dig(d: dict, *keys):
    """Busca la primera clave presente en un dict (tolerante a variantes del payload)."""
    for k in keys:
        if isinstance(d, dict) and d.get(k) not in (None, ""):
            return d[k]
    return None


def parse_inbound(payload: dict) -> Optional[dict]:
    """Normaliza el webhook de YCloud a: {wa_id, telefono, nombre, texto, wa_message_id}.
    Solo procesa mensajes de texto entrantes; devuelve None para el resto (estados, etc.)."""
    if not isinstance(payload, dict):
        return None

    # YCloud v2: evento con objeto `whatsappInboundMessage`. Somos tolerantes a variantes.
    msg = (_dig(payload, "whatsappInboundMessage", "inboundMessage", "message")
           or payload)
    if not isinstance(msg, dict):
        return None

    # Solo mensajes entrantes de texto.
    tipo = (msg.get("type") or "").lower()
    texto_obj = msg.get("text") or {}
    texto = ""
    if isinstance(texto_obj, dict):
        texto = (texto_obj.get("body") or "").strip()
    elif isinstance(texto_obj, str):
        texto = texto_obj.strip()
    if not texto and tipo not in ("text", ""):
        # imagen/audio/etc: por ahora Gero solo maneja texto.
        return None
    if not texto:
        return None

    remitente = _dig(msg, "from", "sender", "waId", "wa_id")
    if not remitente:
        return None
    remitente = str(remitente).lstrip("+")

    perfil = msg.get("customerProfile") or msg.get("profile") or {}
    nombre = _dig(perfil, "name", "nombre") if isinstance(perfil, dict) else None

    wa_message_id = _dig(msg, "id", "messageId", "wamid")

    return {
        "wa_id": remitente,
        "telefono": f"+{remitente}",
        "nombre": nombre,
        "texto": texto,
        "wa_message_id": wa_message_id,
    }


def es_evento_entrante(payload: dict) -> bool:
    """True si el evento del webhook es un mensaje entrante (no un status de entrega/lectura)."""
    tipo = (payload.get("type") or payload.get("event") or "") if isinstance(payload, dict) else ""
    tipo = str(tipo).lower()
    if "inbound" in tipo or "received" in tipo:
        return True
    # Si no viene tipo pero hay un mensaje entrante parseable, lo tratamos como tal.
    return parse_inbound(payload) is not None


def webhook_autorizado(token_recibido: Optional[str]) -> bool:
    """Valida el webhook con un token compartido (header X-Webhook-Token o ?token=).
    Si YCLOUD_WEBHOOK_SECRET no está seteado, deja pasar pero avisa (para desarrollo)."""
    secret = os.getenv("YCLOUD_WEBHOOK_SECRET", "").strip()
    if not secret:
        logger.warning("[gero] YCLOUD_WEBHOOK_SECRET sin configurar: webhook SIN verificar (configuralo en prod).")
        return True
    if not token_recibido:
        return False
    return hmac.compare_digest(secret, token_recibido.strip())
