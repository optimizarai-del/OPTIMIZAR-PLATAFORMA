"""Centro de Agentes — orquestación del equipo de IA desde la plataforma.

Generaliza el patrón del CRM (chat humano↔orquestador + cola de trabajos + fire a
Claude Code sobre el plan, SIN API de Anthropic):

- El humano habla con el ORQUESTADOR por el chat (canal='agentes').
- El orquestador (Claude Code) lee el chat por polling (API key), decide y crea TAREAS
  para los subagentes especializados.
- Cada subagente consume sus tareas pendientes por polling, las ejecuta con sus MCPs y
  devuelve el resultado. El orquestador reporta de vuelta en el chat.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
import os
import logging
import httpx

from app.database import get_db
from app.models import ChatMensaje, AgenteTarea
from app.schemas import (ChatMensajeCreate, ChatMensajeOut,
                         AgenteTareaCreate, AgenteTareaUpdate, AgenteTareaOut,
                         AGENTES_VALIDOS)
from app.security import (get_db_user, verify_api_key, require_manager, require_editor)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/agentes", tags=["agentes"])

CANAL = "agentes"
ESTADOS_CHAT_VALIDOS = {"aprobado", "rechazado", "esperando", "info"}
ESTADOS_TAREA_VALIDOS = {"pendiente", "en_proceso", "completado", "error", "requiere_aprobacion"}


# Catálogo estático del equipo (lo consume la UI para mostrar quién es quién).
# `requiere` describe credenciales/MCP que el agente necesita para operar a pleno.
CATALOGO = [
    {"agente": "investigacion", "nombre": "Investigación",
     "rol": "Monitorea tendencias IA/competidores y arma ideas de contenido.",
     "mcps": ["WebSearch", "WebFetch"], "requiere": None, "listo": True},
    {"agente": "contenido", "nombre": "Contenido",
     "rol": "Genera posts, carruseles y reels para Instagram y LinkedIn.",
     "mcps": ["Instagram Graph API", "LinkedIn API"], "requiere": "Tokens IG/LinkedIn para publicar (genera borradores sin ellos).", "listo": True},
    {"agente": "creativo", "nombre": "Creativo",
     "rol": "Genera prompts e imágenes on-brand para anuncios y orgánico.",
     "mcps": ["ChatGPT Images / Higgsfield"], "requiere": "API de imágenes para generar (deja prompts sin ella).", "listo": True},
    {"agente": "sdr", "nombre": "Prospección (SDR)",
     "rol": "Encuentra prospectos y escribe outreach personalizado.",
     "mcps": ["Apollo", "Instantly"], "requiere": "Apollo/Instantly para envío real.", "listo": True},
    {"agente": "calificacion", "nombre": "Calificación",
     "rol": "Atiende consultas entrantes, califica el lead y agenda.",
     "mcps": ["WhatsApp (WATI)", "Google Calendar"], "requiere": "WhatsApp API + Calendar.", "listo": False},
    {"agente": "crm", "nombre": "CRM",
     "rol": "Actualiza el pipeline y genera alertas de seguimiento.",
     "mcps": ["Supabase", "Notion"], "requiere": None, "listo": True},
    {"agente": "ads", "nombre": "Meta Ads",
     "rol": "Analiza campañas de Meta y recomienda acciones.",
     "mcps": ["Meta Ads (Pipeboard)"], "requiere": "PIPEBOARD_API_TOKEN (ya configurado).", "listo": True},
]


def _fire_orquestador(contenido: str) -> dict:
    """Gatilla la routine del orquestador en el plan (Claude Code online) para que
    responda este mensaje. Sin API de generación: solo dispara la ejecución sobre el plan.
    Si no está configurado, el chat funciona como buzón (lo levanta el ciclo programado)."""
    def _norm(s: str) -> str:
        return (s.replace("—", "-").replace("–", "-").replace("−", "-")
                 .replace("“", '"').replace("”", '"').strip())
    # Permite una routine propia para el orquestador; si no, cae a la genérica del proyecto.
    fire_url = _norm(os.getenv("CLAUDE_ORQUESTADOR_FIRE_URL", "") or os.getenv("CLAUDE_ROUTINE_FIRE_URL", ""))
    token    = _norm(os.getenv("CLAUDE_ROUTINE_TOKEN", ""))
    api_base = _norm(os.getenv("SELF_API_BASE", ""))
    api_key  = _norm(os.getenv("EXTERNAL_API_KEY", ""))
    faltan = [n for n, v in [("FIRE_URL", fire_url), ("TOKEN", token),
                             ("SELF_API_BASE", api_base), ("EXTERNAL_API_KEY", api_key)] if not v]
    if faltan:
        logger.warning(f"[agentes] fire no configurado, faltan: {faltan}")
        return {"ok": False, "motivo": "config_incompleta", "faltan": faltan}
    texto = f"CANAL=agentes\nAPI_BASE={api_base}\nAPI_KEY={api_key}\nMENSAJE: {contenido}"
    try:
        r = httpx.post(fire_url, headers={
            "Authorization": f"Bearer {token}",
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "experimental-cc-routine-2026-04-01",
            "Content-Type": "application/json",
        }, json={"text": texto}, timeout=20)
        logger.info(f"[agentes] fire -> HTTP {r.status_code}")
        return {"ok": r.status_code < 300, "status": r.status_code}
    except Exception as e:
        logger.warning(f"[agentes] fire excepción: {e}")
        return {"ok": False, "motivo": "excepcion", "error": str(e)}


# ── Catálogo del equipo ───────────────────────────────────────────────────────

@router.get("/catalogo")
def catalogo(_=Depends(get_db_user)):
    return CATALOGO


# ── Chat humano ↔ orquestador (canal 'agentes') ───────────────────────────────

@router.get("/chat", response_model=List[ChatMensajeOut])
def listar_chat(db: Session = Depends(get_db), _=Depends(get_db_user)):
    return (db.query(ChatMensaje).filter_by(canal=CANAL)
              .order_by(ChatMensaje.created_at).all())


@router.post("/chat", response_model=ChatMensajeOut)
def postear_humano(data: ChatMensajeCreate, background_tasks: BackgroundTasks,
                   db: Session = Depends(get_db), _=Depends(require_editor)):
    msg = ChatMensaje(canal=CANAL, rol="humano", contenido=data.contenido)
    db.add(msg); db.commit(); db.refresh(msg)
    background_tasks.add_task(_fire_orquestador, data.contenido)
    return msg


@router.patch("/chat/{mid}/estado", response_model=ChatMensajeOut)
def set_estado_chat(mid: int, estado: str, db: Session = Depends(get_db),
                    _=Depends(require_manager)):
    if estado not in ESTADOS_CHAT_VALIDOS:
        raise HTTPException(422, f"Estado inválido. Permitidos: {sorted(ESTADOS_CHAT_VALIDOS)}")
    msg = db.query(ChatMensaje).filter_by(id=mid, canal=CANAL).first()
    if not msg:
        raise HTTPException(404, "Mensaje no encontrado")
    msg.estado = estado
    db.commit(); db.refresh(msg)
    return msg


@router.get("/external/chat", response_model=List[ChatMensajeOut], tags=["agentes-external"])
def listar_chat_externo(limit: int = 50, db: Session = Depends(get_db), _=Depends(verify_api_key)):
    """Lo lee el orquestador (Claude Code) por polling para detectar mensajes humanos sin responder."""
    msgs = (db.query(ChatMensaje).filter_by(canal=CANAL)
              .order_by(ChatMensaje.created_at.desc()).limit(limit).all())
    return list(reversed(msgs))


@router.post("/external/chat", response_model=ChatMensajeOut, tags=["agentes-external"])
def postear_agente(data: ChatMensajeCreate, db: Session = Depends(get_db), _=Depends(verify_api_key)):
    msg = ChatMensaje(
        canal=CANAL, rol="agente", contenido=data.contenido,
        requiere_aprobacion=data.requiere_aprobacion,
        estado="esperando" if data.requiere_aprobacion else "info",
    )
    db.add(msg); db.commit(); db.refresh(msg)
    return msg


# ── Cola de tareas (orquestador → subagentes) ─────────────────────────────────

@router.get("/tareas", response_model=List[AgenteTareaOut])
def listar_tareas(agente: Optional[str] = None, estado: Optional[str] = None,
                  db: Session = Depends(get_db), _=Depends(get_db_user)):
    q = db.query(AgenteTarea)
    if agente:
        q = q.filter(AgenteTarea.agente == agente)
    if estado:
        q = q.filter(AgenteTarea.estado == estado)
    return q.order_by(AgenteTarea.created_at.desc()).limit(200).all()


def _crear_tarea(data: AgenteTareaCreate, db: Session) -> AgenteTarea:
    if data.agente not in AGENTES_VALIDOS:
        raise HTTPException(422, f"Agente inválido. Permitidos: {sorted(AGENTES_VALIDOS)}")
    tarea = AgenteTarea(
        agente=data.agente, instruccion=data.instruccion, contexto=data.contexto,
        prioridad=data.prioridad, origen=data.origen,
    )
    db.add(tarea); db.commit(); db.refresh(tarea)
    return tarea


@router.post("/tareas", response_model=AgenteTareaOut)
def crear_tarea(data: AgenteTareaCreate, db: Session = Depends(get_db), _=Depends(require_editor)):
    """El humano puede encargar una tarea directa a un subagente (sin pasar por el chat)."""
    data.origen = "humano"
    return _crear_tarea(data, db)


@router.post("/external/tareas", response_model=AgenteTareaOut, tags=["agentes-external"])
def crear_tarea_externa(data: AgenteTareaCreate, db: Session = Depends(get_db), _=Depends(verify_api_key)):
    """El orquestador (Claude Code) encola tareas para los subagentes."""
    return _crear_tarea(data, db)


@router.get("/external/tareas/pending", response_model=List[AgenteTareaOut], tags=["agentes-external"])
def tareas_pendientes(agente: Optional[str] = None, db: Session = Depends(get_db), _=Depends(verify_api_key)):
    """Cada subagente pide sus tareas pendientes (filtrando por su nombre)."""
    q = db.query(AgenteTarea).filter(AgenteTarea.estado == "pendiente")
    if agente:
        q = q.filter(AgenteTarea.agente == agente)
    return q.order_by(AgenteTarea.created_at).all()


@router.patch("/external/tareas/{tid}", response_model=AgenteTareaOut, tags=["agentes-external"])
def actualizar_tarea(tid: int, data: AgenteTareaUpdate, db: Session = Depends(get_db), _=Depends(verify_api_key)):
    """El subagente actualiza el estado/resultado de su tarea."""
    tarea = db.query(AgenteTarea).filter_by(id=tid).first()
    if not tarea:
        raise HTTPException(404, "Tarea no encontrada")
    if data.estado is not None:
        if data.estado not in ESTADOS_TAREA_VALIDOS:
            raise HTTPException(422, f"Estado inválido. Permitidos: {sorted(ESTADOS_TAREA_VALIDOS)}")
        tarea.estado = data.estado
        if data.estado in ("completado", "error"):
            tarea.processed_at = datetime.now(timezone.utc)
    if data.resultado is not None:
        tarea.resultado = data.resultado
    db.commit(); db.refresh(tarea)
    return tarea
