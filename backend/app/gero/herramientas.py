"""Las herramientas de Gero (tool-use de Anthropic) que operan sobre el CRM.

Cada tool tiene (1) un esquema en formato Anthropic para el modelo y (2) un ejecutor
que corre en el backend con una sesión de DB. Los ejecutores devuelven un string corto
que se le pasa de vuelta al modelo como `tool_result` (traza, no se le muestra al cliente).
"""
import os
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models import Contacto, GeroConversacion, ChatMensaje

logger = logging.getLogger(__name__)

CALENDLY_URL = os.getenv("CALENDLY_URL", "https://calendly.com/optimizar-ai/30min")

# Niveles de interés válidos (evita valores arbitrarios del modelo).
NIVELES = {"frio", "tibio", "caliente"}
# Estados de contacto que Gero puede setear.
ESTADOS_CONTACTO = {"nuevo", "contactado", "respondido", "baja"}


# ── Esquemas de las tools (formato Anthropic Messages API) ────────────────────

TOOLS = [
    {
        "name": "guardar_prospecto",
        "description": ("Registra o actualiza al prospecto en el CRM de OPTIMIZAR. Usala apenas "
                        "sepas algo concreto (empresa, nombre, rubro o qué necesita). Es idempotente: "
                        "podés llamarla varias veces a medida que te enterás de más cosas."),
        "input_schema": {
            "type": "object",
            "properties": {
                "empresa": {"type": "string", "description": "Nombre de la empresa o, si es particular, su nombre."},
                "nombre": {"type": "string", "description": "Nombre de la persona con la que hablás."},
                "email": {"type": "string", "description": "Email, si lo comparte."},
                "rubro": {"type": "string", "description": "Rubro o sector de la empresa."},
                "necesidad": {"type": "string", "description": "Qué problema quiere resolver / qué está buscando, en 1-2 frases."},
            },
            "required": ["empresa"],
        },
    },
    {
        "name": "clasificar_prospecto",
        "description": ("Clasifica el nivel de interés del prospecto según cómo viene la charla. "
                        "Actualizala a medida que avanza la conversación."),
        "input_schema": {
            "type": "object",
            "properties": {
                "nivel_interes": {"type": "string", "enum": ["frio", "tibio", "caliente"],
                                  "description": "frio = curiosea/no decide; tibio = interés real; caliente = quiere avanzar/agendar."},
                "motivo": {"type": "string", "description": "Por qué lo clasificás así, breve."},
            },
            "required": ["nivel_interes"],
        },
    },
    {
        "name": "agregar_nota",
        "description": ("Deja una nota u observación en el CRM para que el equipo tenga contexto "
                        "(objeciones, presupuesto que mencionó, urgencia, detalles del proyecto, etc.)."),
        "input_schema": {
            "type": "object",
            "properties": {
                "nota": {"type": "string", "description": "La observación a registrar."},
            },
            "required": ["nota"],
        },
    },
    {
        "name": "compartir_calendly",
        "description": ("Marca que le vas a ofrecer agendar una reunión de 30 min y te devuelve el link "
                        "de Calendly para que lo incluyas en tu mensaje. Usala cuando haya interés real."),
        "input_schema": {
            "type": "object",
            "properties": {
                "motivo": {"type": "string", "description": "Contexto de por qué agendan (para la nota del CRM)."},
            },
            "required": [],
        },
    },
    {
        "name": "handoff_humano",
        "description": ("Escala la conversación a una persona del equipo. Usala si el cliente lo pide, "
                        "si es un tema delicado, un reclamo, o algo que no podés resolver."),
        "input_schema": {
            "type": "object",
            "properties": {
                "motivo": {"type": "string", "description": "Por qué lo pasás a un humano."},
            },
            "required": ["motivo"],
        },
    },
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")


def _get_or_create_contacto(conv: GeroConversacion, db: Session, empresa: str) -> Contacto:
    """Devuelve el Contacto vinculado a la conversación; si no existe, lo crea.
    Idempotente por external_id = 'wa:<wa_id>'."""
    if conv.contacto_id:
        c = db.query(Contacto).filter_by(id=conv.contacto_id).first()
        if c:
            return c
        conv.contacto_id = None  # puntero colgado

    ext = f"wa:{conv.wa_id}"
    c = db.query(Contacto).filter_by(external_id=ext).first()
    if not c:
        c = Contacto(
            empresa=empresa or (conv.nombre_perfil or "Contacto WhatsApp"),
            nombre=conv.nombre_perfil,
            telefono=conv.telefono or conv.wa_id,
            origen="whatsapp",
            estado="respondido",   # escribió por WhatsApp: ya es un lead activo
            external_id=ext,
            idioma="es",
        )
        db.add(c)
        db.flush()
    conv.contacto_id = c.id
    return c


def _append_info(c: Contacto, linea: str) -> None:
    """Agrega una línea con timestamp al campo `info` del contacto (bitácora de notas)."""
    prefijo = f"[{_now_str()}] "
    c.info = (f"{c.info}\n{prefijo}{linea}" if c.info else f"{prefijo}{linea}")


# ── Ejecutores ────────────────────────────────────────────────────────────────

def _guardar_prospecto(args: dict, db: Session, conv: GeroConversacion) -> str:
    empresa = (args.get("empresa") or "").strip()
    c = _get_or_create_contacto(conv, db, empresa)
    if empresa:
        c.empresa = empresa
    if args.get("nombre"):
        c.nombre = args["nombre"].strip()
    if args.get("email"):
        c.email = args["email"].strip()
    # rubro + necesidad se acumulan en la bitácora `info`.
    detalle = " · ".join(x for x in (
        (f"Rubro: {args['rubro']}" if args.get("rubro") else ""),
        (f"Necesidad: {args['necesidad']}" if args.get("necesidad") else ""),
    ) if x)
    if detalle:
        _append_info(c, detalle)
    db.flush()
    return f"OK: prospecto '{c.empresa}' guardado en el CRM (contacto_id={c.id})."


def _clasificar_prospecto(args: dict, db: Session, conv: GeroConversacion) -> str:
    nivel = (args.get("nivel_interes") or "").strip().lower()
    if nivel not in NIVELES:
        return f"Error: nivel_interes debe ser uno de {sorted(NIVELES)}."
    conv.nivel_interes = nivel
    c = _get_or_create_contacto(conv, db, conv.nombre_perfil or "Contacto WhatsApp")
    motivo = args.get("motivo") or ""
    _append_info(c, f"Clasificado como {nivel.upper()}" + (f" — {motivo}" if motivo else ""))
    db.flush()
    return f"OK: interés = {nivel}."


def _agregar_nota(args: dict, db: Session, conv: GeroConversacion) -> str:
    nota = (args.get("nota") or "").strip()
    if not nota:
        return "Error: la nota está vacía."
    c = _get_or_create_contacto(conv, db, conv.nombre_perfil or "Contacto WhatsApp")
    _append_info(c, f"Nota: {nota}")
    db.flush()
    return "OK: nota registrada en el CRM."


def _compartir_calendly(args: dict, db: Session, conv: GeroConversacion) -> str:
    conv.nivel_interes = "caliente"
    c = _get_or_create_contacto(conv, db, conv.nombre_perfil or "Contacto WhatsApp")
    motivo = args.get("motivo") or "quiere avanzar"
    _append_info(c, f"Se le ofreció agendar reunión ({motivo}).")
    db.flush()
    # El link se le devuelve al modelo para que lo incluya en su mensaje al cliente.
    return f"OK: prospecto marcado CALIENTE. Pasale este link de agenda: {CALENDLY_URL}"


def _handoff_humano(args: dict, db: Session, conv: GeroConversacion) -> str:
    motivo = (args.get("motivo") or "sin especificar").strip()
    conv.estado = "handoff_humano"
    c = _get_or_create_contacto(conv, db, conv.nombre_perfil or "Contacto WhatsApp")
    _append_info(c, f"⚠️ Handoff a humano solicitado: {motivo}")
    # Avisa en el chat de la plataforma (canal 'agentes') para que alguien lo tome.
    nombre = c.nombre or conv.nombre_perfil or conv.telefono or conv.wa_id
    db.add(ChatMensaje(
        canal="agentes",
        rol="sistema",
        contenido=(f"🙋 Gero pide handoff humano en WhatsApp — {nombre} "
                   f"(contacto_id={c.id}, tel {conv.telefono or conv.wa_id}). Motivo: {motivo}"),
        requiere_aprobacion=False,
        estado="info",
    ))
    db.flush()
    return "OK: conversación escalada a un humano. Avisale al cliente que en breve lo contacta alguien del equipo."


_EJECUTORES = {
    "guardar_prospecto": _guardar_prospecto,
    "clasificar_prospecto": _clasificar_prospecto,
    "agregar_nota": _agregar_nota,
    "compartir_calendly": _compartir_calendly,
    "handoff_humano": _handoff_humano,
}


def ejecutar_tool(nombre: str, args: dict, db: Session, conv: GeroConversacion) -> str:
    """Ejecuta una tool por nombre. Nunca levanta excepción hacia el loop: si algo falla,
    devuelve un string de error para que el modelo lo maneje y siga la charla."""
    fn = _EJECUTORES.get(nombre)
    if not fn:
        return f"Error: herramienta desconocida '{nombre}'."
    try:
        return fn(args or {}, db, conv)
    except Exception as e:  # defensivo: una tool rota no debe tumbar la respuesta de Gero
        logger.exception("[gero] tool '%s' falló: %s", nombre, e)
        return f"Error al ejecutar '{nombre}': {e}"
