import os
import re
import json
import httpx
from typing import Literal

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-4-5-20251001"

# Confianza mínima para aceptar la clasificación del modelo.
# Por debajo de este umbral se retorna consulta_general como fallback seguro
# para evitar actuar sobre intenciones ambiguas (ej: disparar generar_contrato
# con 0.5 de confianza podría iniciar un flujo crítico por error).
CONFIDENCE_THRESHOLD = 0.7

Intent = Literal["buscar_propiedad", "agendar_visita", "generar_contrato", "consulta_general"]

INTENT_TOOL = {
    "name": "clasificar_intencion",
    "description": (
        "Clasificá la intención principal del mensaje de un usuario en el contexto "
        "de una inmobiliaria boutique de Buenos Aires."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "intent": {
                "type": "string",
                "enum": ["buscar_propiedad", "agendar_visita", "generar_contrato", "consulta_general"],
                "description": (
                    "buscar_propiedad: quiere ver o filtrar propiedades disponibles. "
                    "agendar_visita: quiere coordinar una visita a una propiedad. "
                    "generar_contrato: quiere iniciar reserva, contrato de alquiler o compraventa. "
                    "consulta_general: pregunta sobre precios, zonas, trámites, expensas u otra cosa."
                ),
            },
            "confidence": {
                "type": "number",
                "description": "Confianza en la clasificación, entre 0.0 y 1.0.",
            },
            "extracted_data": {
                "type": "object",
                "description": (
                    "Datos relevantes extraídos del mensaje según la intención. "
                    "Ejemplos: zona, tipo_propiedad, presupuesto, operacion (venta/alquiler), "
                    "ambientes, fecha_visita, property_id."
                ),
                "additionalProperties": True,
            },
        },
        "required": ["intent", "confidence", "extracted_data"],
    },
}


def route_intent(message: str, conversation_history: list[dict] | None = None) -> dict:
    """
    Clasifica la intención del mensaje usando Claude tool_use.

    Args:
        message: Texto del mensaje entrante del usuario.
        conversation_history: Lista de mensajes previos [{role, content}] para contexto.
                              Se trunca a los últimos 6 turnos para no saturar el contexto.

    Returns:
        {
            "intent": Intent,
            "confidence": float,
            "extracted_data": dict,
            "error": str | None
        }
    """
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        return _fallback_intent(message)

    history = (conversation_history or [])[-6:]

    messages = history + [{"role": "user", "content": message}]

    try:
        resp = httpx.post(
            ANTHROPIC_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": MODEL,
                "max_tokens": 512,
                "tools": [INTENT_TOOL],
                "tool_choice": {"type": "tool", "name": "clasificar_intencion"},
                "system": (
                    "Sos un clasificador de intenciones para una inmobiliaria boutique de Buenos Aires. "
                    "Tu única tarea es identificar qué quiere hacer el usuario y extraer datos relevantes. "
                    "Usá la herramienta clasificar_intencion con precisión."
                ),
                "messages": messages,
            },
            timeout=30,
        )
        resp.raise_for_status()

        content = resp.json().get("content", [])
        tool_use_block = next((b for b in content if b.get("type") == "tool_use"), None)
        if not tool_use_block:
            return _fallback_intent(message)

        result = tool_use_block["input"]
        confidence = float(result.get("confidence", 0.8))

        # Si la confianza es baja, descartar la clasificación y retornar
        # consulta_general como fallback seguro para evitar flujos críticos
        # (ej: generar_contrato) disparados por clasificaciones ambiguas.
        if confidence < CONFIDENCE_THRESHOLD:
            return {
                "intent": "consulta_general",
                "confidence": confidence,
                "extracted_data": result.get("extracted_data", {}),
                "error": None,
            }

        return {
            "intent": result["intent"],
            "confidence": confidence,
            "extracted_data": result.get("extracted_data", {}),
            "error": None,
        }

    except httpx.HTTPStatusError as e:
        return {**_fallback_intent(message), "error": f"API {e.response.status_code}: {e.response.text[:200]}"}
    except Exception as e:
        return {**_fallback_intent(message), "error": str(e)}


def _kw_match(text: str, keywords: list[str]) -> bool:
    """Coincidencia con word boundaries para evitar falsos positivos por substring."""
    return any(re.search(r'\b' + re.escape(k) + r'\b', text) for k in keywords)


def _fallback_intent(message: str) -> dict:
    """
    Clasificación determinística por keywords cuando la API no está disponible.
    Usa word boundaries para evitar falsos positivos (ej: "zona" en "zonas").
    Prioridad: visita > búsqueda > contrato > general (búsqueda antes de contrato
    porque "busco para alquilar" es búsqueda, no inicio de contrato).
    """
    text = message.lower()

    visita_kw = ["visita", "ver la propiedad", "conocer el depto", "puedo ir", "cuando puedo", "agendar"]
    # "alquilar" solo no es suficiente para inferir contrato; se usan frases más específicas
    contrato_kw = ["contrato", "reserva", "firmar", "hacer la oferta", "iniciar reserva", "cerrar trato"]
    busqueda_kw = ["busco", "necesito", "quiero comprar", "quiero alquilar", "tienen algo",
                   "propiedades", "departamento", "casa", "oficina", "local", "terreno",
                   "zona", "barrio", "ambientes", "metros", "precio", "presupuesto"]

    if _kw_match(text, visita_kw):
        intent = "agendar_visita"
    elif _kw_match(text, busqueda_kw):
        intent = "buscar_propiedad"
    elif _kw_match(text, contrato_kw):
        intent = "generar_contrato"
    else:
        intent = "consulta_general"

    return {
        "intent": intent,
        "confidence": 0.6,
        "extracted_data": {},
        "error": None,
    }
