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

# Un canal de chat por Director IA: cada uno trabaja independiente, con su propia routine y clave.
AREAS = {"marketing", "comercial", "desarrollo"}
CANAL_DEFAULT = "comercial"
ESTADOS_CHAT_VALIDOS = {"aprobado", "rechazado", "esperando", "info"}
ESTADOS_TAREA_VALIDOS = {"pendiente", "en_proceso", "completado", "error", "requiere_aprobacion"}


# Catálogo estático del equipo (lo consume la UI). Organizado en 3 áreas, cada una con su
# Director IA. `area` agrupa; `director` marca al cerebro del área. `requiere` describe la
# credencial/MCP que falta para operar a pleno.
CATALOGO = [
    # ── MARKETING ──
    {"area": "Marketing", "agente": "director-marketing", "nombre": "Director de Marketing", "director": True,
     "rol": "Planifica la semana de contenido, coordina su equipo y reporta.",
     "mcps": [], "requiere": None, "listo": True},
    {"area": "Marketing", "agente": "investigacion", "nombre": "Investigador",
     "rol": "Tendencias IA/competidores → briefing semanal de ideas.",
     "mcps": ["WebSearch", "Google Trends"], "requiere": None, "listo": True},
    {"area": "Marketing", "agente": "contenido", "nombre": "Contenido",
     "rol": "Copy de posts para Instagram y LinkedIn según pilar.",
     "mcps": ["Claude"], "requiere": None, "listo": True},
    {"area": "Marketing", "agente": "creativo", "nombre": "Creativo",
     "rol": "Prompts e imágenes on-brand.",
     "mcps": ["ChatGPT Images / Higgsfield"], "requiere": "API de imágenes para generar (deja prompts sin ella).", "listo": True},
    {"area": "Marketing", "agente": "programador", "nombre": "Programador",
     "rol": "Publica las piezas aprobadas y gestiona el calendario.",
     "mcps": ["Instagram Graph API", "LinkedIn API"], "requiere": "Tokens IG/LinkedIn para publicar.", "listo": False},
    {"area": "Marketing", "agente": "metricas", "nombre": "Métricas",
     "rol": "Performance de cada pieza; detecta qué funciona.",
     "mcps": ["Meta API", "LinkedIn API"], "requiere": "Acceso a métricas de IG/LinkedIn.", "listo": False},
    {"area": "Marketing", "agente": "ads", "nombre": "Meta Ads",
     "rol": "Analiza campañas de Meta (paga) y recomienda acciones.",
     "mcps": ["Meta Ads (Pipeboard)"], "requiere": "PIPEBOARD_API_TOKEN (ya configurado).", "listo": True},

    # ── COMERCIAL ──
    {"area": "Comercial", "agente": "director-comercial", "nombre": "Director Comercial", "director": True,
     "rol": "Corre prospección y calificación, mantiene el pipeline.",
     "mcps": [], "requiere": None, "listo": True},
    {"area": "Comercial", "agente": "sdr", "nombre": "Prospección (SDR)",
     "rol": "Encuentra prospectos y escribe outreach. Carga a Contactos.",
     "mcps": ["Apollo", "Instantly"], "requiere": "Apollo/Instantly para envío real.", "listo": True},
    {"area": "Comercial", "agente": "calificacion", "nombre": "Calificador",
     "rol": "Atiende entrantes, califica y pasa al pipeline.",
     "mcps": ["WhatsApp (WATI)"], "requiere": "WhatsApp API.", "listo": False},
    {"area": "Comercial", "agente": "agenda", "nombre": "Agenda",
     "rol": "Agenda reuniones de diagnóstico con leads calificados.",
     "mcps": ["Google Calendar"], "requiere": "Google Calendar.", "listo": False},
    {"area": "Comercial", "agente": "crm", "nombre": "CRM",
     "rol": "Actualiza el pipeline y genera alertas de seguimiento.",
     "mcps": ["Supabase", "Notion"], "requiere": None, "listo": True},
    {"area": "Comercial", "agente": "propuestas", "nombre": "Propuestas",
     "rol": "Borrador de propuesta comercial personalizada.",
     "mcps": ["Claude"], "requiere": None, "listo": True},

    # ── DESARROLLO ──
    {"area": "Desarrollo", "agente": "director-desarrollo", "nombre": "Director de Desarrollo", "director": True,
     "rol": "Coordina el ciclo de entrega: diagnóstico → desarrollo → QA → deploy → mantenimiento.",
     "mcps": [], "requiere": None, "listo": True},
    {"area": "Desarrollo", "agente": "relevador", "nombre": "Relevador Técnico",
     "rol": "Requerimiento → spec técnica + estimación + servicio que lo cubre.",
     "mcps": ["Requerimientos", "Servicios"], "requiere": None, "listo": True},
    {"area": "Desarrollo", "agente": "planificador", "nombre": "Planificador",
     "rol": "Del spec arma el plan de acción + tareas del proyecto.",
     "mcps": ["Proyectos", "Tareas"], "requiere": None, "listo": True},
    {"area": "Desarrollo", "agente": "desarrollador", "nombre": "Desarrollador",
     "rol": "Implementa el código del módulo sobre el repo del proyecto.",
     "mcps": ["GitHub", "Claude Code"], "requiere": None, "listo": True},
    {"area": "Desarrollo", "agente": "revisor", "nombre": "Revisor de Código",
     "rol": "Revisa el diff antes de mergear (bugs, calidad, reuso).",
     "mcps": ["Claude Code"], "requiere": None, "listo": True},
    {"area": "Desarrollo", "agente": "qa", "nombre": "QA / Testing",
     "rol": "Prueba la solución, busca edge cases y reporta bugs.",
     "mcps": ["Claude Code"], "requiere": None, "listo": True},
    {"area": "Desarrollo", "agente": "devops", "nombre": "DevOps / Deploy",
     "rol": "Despliega en EasyPanel, configura env, verifica salud.",
     "mcps": ["EasyPanel"], "requiere": "Deploy a prod requiere aprobación humana.", "listo": True},
    {"area": "Desarrollo", "agente": "soporte", "nombre": "Soporte / Mantenimiento",
     "rol": "Monitorea producción, triage de bugs, mantenimiento mensual.",
     "mcps": ["Logs", "Supabase"], "requiere": None, "listo": True},
    {"area": "Desarrollo", "agente": "documentador", "nombre": "Documentador",
     "rol": "Doc técnica + manual de entrega para el cliente.",
     "mcps": ["Drive"], "requiere": None, "listo": True},
]


def _fire_director(canal: str, contenido: str) -> dict:
    """Gatilla la routine del Director del área `canal` (marketing/comercial/desarrollo) sobre
    el plan de Claude. Cada director tiene su propia fire URL y su propia API key. Si no está
    configurado, el chat funciona como buzón (lo levanta el ciclo programado del director)."""
    def _norm(s: str) -> str:
        return (s.replace("—", "-").replace("–", "-").replace("−", "-")
                 .replace("“", '"').replace("”", '"').strip())
    area = canal if canal in AREAS else CANAL_DEFAULT
    # Fire URL del director del área; cae a la genérica si no está la específica.
    fire_url = _norm(os.getenv(f"CLAUDE_FIRE_{area.upper()}", "")
                     or os.getenv("CLAUDE_ORQUESTADOR_FIRE_URL", ""))
    token    = _norm(os.getenv("CLAUDE_ROUTINE_TOKEN", ""))
    api_base = _norm(os.getenv("SELF_API_BASE", ""))
    # API key propia del área; cae a la global.
    api_key  = _norm(os.getenv(f"EXTERNAL_API_KEY_{area.upper()}", "")
                     or os.getenv("EXTERNAL_API_KEY", ""))
    faltan = [n for n, v in [("FIRE_URL", fire_url), ("TOKEN", token),
                             ("SELF_API_BASE", api_base), ("API_KEY", api_key)] if not v]
    if faltan:
        logger.warning(f"[agentes:{area}] fire no configurado, faltan: {faltan}")
        return {"ok": False, "motivo": "config_incompleta", "faltan": faltan}
    texto = f"CANAL={area}\nAPI_BASE={api_base}\nAPI_KEY={api_key}\nMENSAJE: {contenido}"
    try:
        r = httpx.post(fire_url, headers={
            "Authorization": f"Bearer {token}",
            "anthropic-version": "2023-06-01",
            "anthropic-beta": "experimental-cc-routine-2026-04-01",
            "Content-Type": "application/json",
        }, json={"text": texto}, timeout=20)
        logger.info(f"[agentes:{area}] fire -> HTTP {r.status_code}")
        return {"ok": r.status_code < 300, "status": r.status_code}
    except Exception as e:
        logger.warning(f"[agentes:{area}] fire excepción: {e}")
        return {"ok": False, "motivo": "excepcion", "error": str(e)}


# ── Catálogo del equipo ───────────────────────────────────────────────────────

@router.get("/catalogo")
def catalogo(_=Depends(get_db_user)):
    return CATALOGO


# ── Chat humano ↔ orquestador (canal 'agentes') ───────────────────────────────

def _canal_valido(canal: str) -> str:
    return canal if canal in AREAS else CANAL_DEFAULT


@router.get("/chat", response_model=List[ChatMensajeOut])
def listar_chat(canal: str = CANAL_DEFAULT, db: Session = Depends(get_db), _=Depends(get_db_user)):
    return (db.query(ChatMensaje).filter_by(canal=_canal_valido(canal))
              .order_by(ChatMensaje.created_at).all())


@router.post("/chat", response_model=ChatMensajeOut)
def postear_humano(data: ChatMensajeCreate, background_tasks: BackgroundTasks,
                   db: Session = Depends(get_db), _=Depends(require_editor)):
    canal = _canal_valido(data.canal)
    msg = ChatMensaje(canal=canal, rol="humano", contenido=data.contenido)
    db.add(msg); db.commit(); db.refresh(msg)
    # Dispara al Director del área correspondiente (su routine + su API key).
    background_tasks.add_task(_fire_director, canal, data.contenido)
    return msg


@router.patch("/chat/{mid}/estado", response_model=ChatMensajeOut)
def set_estado_chat(mid: int, estado: str, db: Session = Depends(get_db),
                    _=Depends(require_manager)):
    if estado not in ESTADOS_CHAT_VALIDOS:
        raise HTTPException(422, f"Estado inválido. Permitidos: {sorted(ESTADOS_CHAT_VALIDOS)}")
    msg = db.query(ChatMensaje).filter_by(id=mid).first()
    if not msg:
        raise HTTPException(404, "Mensaje no encontrado")
    msg.estado = estado
    db.commit(); db.refresh(msg)
    return msg


@router.get("/external/chat", response_model=List[ChatMensajeOut], tags=["agentes-external"])
def listar_chat_externo(canal: str = CANAL_DEFAULT, limit: int = 50,
                        db: Session = Depends(get_db), _=Depends(verify_api_key)):
    """Lo lee el Director (Claude Code) por polling para detectar mensajes humanos sin responder.
    Cada director consulta su propio canal."""
    msgs = (db.query(ChatMensaje).filter_by(canal=_canal_valido(canal))
              .order_by(ChatMensaje.created_at.desc()).limit(limit).all())
    return list(reversed(msgs))


@router.post("/external/chat", response_model=ChatMensajeOut, tags=["agentes-external"])
def postear_agente(data: ChatMensajeCreate, db: Session = Depends(get_db), _=Depends(verify_api_key)):
    msg = ChatMensaje(
        canal=_canal_valido(data.canal), rol="agente", contenido=data.contenido,
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
