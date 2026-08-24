"""El cerebro de Gero: loop de conversación con la API de Anthropic (tool-use) + memoria en DB.

Excepción documentada al patrón "sin API de Anthropic": Gero responde en tiempo real al
webhook de WhatsApp, así que usa la Messages API directo por httpx (igual que ai_service.py),
NO las routines de Claude Code.
"""
import os
import json
import logging
from datetime import datetime, timezone
from typing import Optional

import httpx
from sqlalchemy.orm import Session

from app.models import GeroConversacion, GeroMensaje
from app.gero import personalidad, herramientas, diagnostico

logger = logging.getLogger(__name__)

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL = os.getenv("GERO_MODEL", "claude-haiku-4-5-20251001")

# Cuántos mensajes recientes se le pasan al modelo como memoria de trabajo.
# El historial completo queda siempre en la DB (memoria larga).
MAX_HISTORIAL = 24
# Tope de vueltas del loop de tools (anti bucle infinito).
MAX_ITERACIONES = 6


def _anthropic(system: str, messages: list, tools: list) -> Optional[dict]:
    """POST crudo a la Messages API. Devuelve el JSON o None si falla."""
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        logger.error("[gero] ANTHROPIC_API_KEY no configurada.")
        return None
    try:
        r = httpx.post(
            ANTHROPIC_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": MODEL,
                "max_tokens": 1024,
                "system": system,
                "messages": messages,
                "tools": tools,
            },
            timeout=60,
        )
        r.raise_for_status()
        return r.json()
    except httpx.HTTPStatusError as e:
        logger.error("[gero] Anthropic %s: %s", e.response.status_code, e.response.text[:300])
        return None
    except Exception as e:
        logger.error("[gero] Anthropic excepción: %s", e)
        return None


def obtener_conversacion(db: Session, wa_id: str, telefono: str = None,
                         nombre: str = None) -> GeroConversacion:
    """Trae la conversación por wa_id o la crea. Actualiza nombre/teléfono si llegan nuevos."""
    conv = db.query(GeroConversacion).filter_by(wa_id=wa_id).first()
    if not conv:
        conv = GeroConversacion(wa_id=wa_id, telefono=telefono, nombre_perfil=nombre)
        db.add(conv)
        db.flush()
        return conv
    if telefono and not conv.telefono:
        conv.telefono = telefono
    if nombre and not conv.nombre_perfil:
        conv.nombre_perfil = nombre
    return conv


def _ya_procesado(db: Session, wa_message_id: str) -> bool:
    """Idempotencia: ¿ya guardamos este mensaje entrante de WhatsApp?"""
    if not wa_message_id:
        return False
    return db.query(GeroMensaje.id).filter_by(wa_message_id=wa_message_id).first() is not None


def _historial_para_modelo(conv: GeroConversacion, db: Session) -> list:
    """Últimos N mensajes como memoria de trabajo, en formato Anthropic (solo texto)."""
    filas = (db.query(GeroMensaje)
               .filter_by(conversacion_id=conv.id)
               .order_by(GeroMensaje.created_at.desc())
               .limit(MAX_HISTORIAL)
               .all())
    filas.reverse()
    return [{"role": m.rol, "content": m.contenido} for m in filas]


def _texto_de(content_blocks: list) -> str:
    """Concatena los bloques de texto de una respuesta del modelo."""
    return "\n".join(b.get("text", "") for b in content_blocks if b.get("type") == "text").strip()


def responder(db: Session, wa_id: str, texto: str, telefono: str = None,
              nombre: str = None, wa_message_id: str = None) -> Optional[str]:
    """Procesa un mensaje entrante y devuelve la respuesta de Gero (o None si no hay que
    responder: duplicado, conversación en handoff, o error irrecuperable).

    Persiste el turno entrante y el saliente en la DB (memoria). Ejecuta las tools del CRM.
    """
    conv = obtener_conversacion(db, wa_id, telefono, nombre)

    # Idempotencia: si YCloud reintrega el mismo mensaje, no lo reprocesamos.
    if _ya_procesado(db, wa_message_id):
        db.commit()
        logger.info("[gero] mensaje %s ya procesado, se ignora.", wa_message_id)
        return None

    # Guardamos el mensaje entrante (memoria). Flush explícito: la sesión tiene
    # autoflush=False, así que sin esto el historial que armamos abajo no lo vería.
    db.add(GeroMensaje(conversacion_id=conv.id, rol="user", contenido=texto,
                       wa_message_id=wa_message_id))
    conv.ultima_actividad = datetime.now(timezone.utc)
    db.flush()

    # Si la charla está en manos de un humano, Gero no pisa la conversación.
    if conv.estado == "handoff_humano":
        db.commit()
        logger.info("[gero] conv %s en handoff humano; Gero no responde.", conv.id)
        return None

    # ── Armamos el contexto para el modelo ──
    # Si la persona viene del embudo del diagnóstico, su mensaje trae el código.
    # Le cargamos la ficha completa ANTES de que hable: no la buscamos con una
    # herramienta porque si el modelo se olvidara de llamarla, el primer mensaje
    # —el que más pesa— saldría genérico. Va después del flush de arriba, así el
    # mensaje recién llegado ya entra en la búsqueda.
    codigo = diagnostico.token_de_conversacion(db, conv.id)
    ficha = diagnostico.contexto(db, codigo) if codigo else None
    if ficha:
        logger.info("[gero] conv %s viene del diagnóstico %s", conv.id, codigo)

    system = personalidad.system_prompt(
        nombre_contacto=(conv.nombre_perfil or nombre),
        resumen_previo=conv.resumen,
        diagnostico=ficha,
    )
    messages = _historial_para_modelo(conv, db)

    # ── Loop de tool-use ──
    traza_tools = []
    texto_final = ""
    for _ in range(MAX_ITERACIONES):
        resp = _anthropic(system, messages, herramientas.TOOLS)
        if not resp:
            break
        blocks = resp.get("content", [])
        texto_final = _texto_de(blocks) or texto_final

        if resp.get("stop_reason") != "tool_use":
            break

        # Registramos el turno del asistente (con sus tool_use) y ejecutamos las tools.
        messages.append({"role": "assistant", "content": blocks})
        tool_results = []
        for b in blocks:
            if b.get("type") != "tool_use":
                continue
            nombre_tool, args, tid = b.get("name"), b.get("input", {}), b.get("id")
            resultado = herramientas.ejecutar_tool(nombre_tool, args, db, conv)
            traza_tools.append({"tool": nombre_tool, "input": args, "result": resultado})
            tool_results.append({"type": "tool_result", "tool_use_id": tid, "content": resultado})
        messages.append({"role": "user", "content": tool_results})

    if not texto_final:
        texto_final = ("¡Perdón! Se me cruzaron los cables un segundo 🙈 "
                       "¿Me lo repetís así te ayudo?")

    # Persistimos la respuesta de Gero (memoria).
    db.add(GeroMensaje(conversacion_id=conv.id, rol="assistant", contenido=texto_final,
                       herramientas=traza_tools or None))
    conv.ultima_actividad = datetime.now(timezone.utc)
    db.commit()
    return texto_final
