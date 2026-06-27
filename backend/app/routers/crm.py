from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timezone
import os
import logging
import httpx
from app.database import get_db
from app.models import (Oportunidad, EtapaOportunidad, FuenteOportunidad,
                        Proyecto, ProyectoStatus, User, UserRole,
                        LeadJob, ChatMensaje, Contacto)
from app.schemas import (OportunidadCreate, OportunidadUpdate, OportunidadOut,
                         OportunidadExternal, CRMStats, ProyectoOut,
                         LeadJobCreate, LeadJobUpdate, LeadJobOut,
                         ChatMensajeCreate, ChatMensajeOut, FunnelNotify,
                         RespuestaInbound,
                         ContactoCreate, ContactoUpdate, ContactoOut, ContactoExternal)
from app.security import get_db_user, verify_api_key, require_manager, require_editor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/crm", tags=["crm"])


def _fire_chat_responder(contenido: str) -> dict:
    """Dispara la routine 'chat-responder' en el plan (Claude Code online) para que el
    orquestador responda este mensaje en el chat. Corre en background; si no está
    configurado, no hace nada (el chat queda como buzón). Sin API de generación: el /fire
    solo gatilla la ejecución, que corre sobre el plan. Devuelve un dict de diagnóstico."""
    # Normaliza guiones/comillas "inteligentes" que rompen el header (em/en dash → '-').
    def _norm(s: str) -> str:
        return (s.replace("—", "-").replace("–", "-").replace("−", "-")
                 .replace("“", '"').replace("”", '"').strip())
    fire_url = _norm(os.getenv("CLAUDE_ROUTINE_FIRE_URL", ""))
    token    = _norm(os.getenv("CLAUDE_ROUTINE_TOKEN", ""))
    api_base = _norm(os.getenv("SELF_API_BASE", ""))    # URL PÚBLICA del backend
    api_key  = _norm(os.getenv("EXTERNAL_API_KEY", ""))
    faltan = [n for n, v in [("CLAUDE_ROUTINE_FIRE_URL", fire_url),
                             ("CLAUDE_ROUTINE_TOKEN", token),
                             ("SELF_API_BASE", api_base),
                             ("EXTERNAL_API_KEY", api_key)] if not v]
    if faltan:
        logger.warning(f"[chat] fire no configurado, faltan env: {faltan}")
        return {"ok": False, "motivo": "config_incompleta", "faltan": faltan}
    texto = f"API_BASE={api_base}\nAPI_KEY={api_key}\nMENSAJE: {contenido}"
    try:
        r = httpx.post(
            fire_url,
            headers={
                "Authorization": f"Bearer {token}",
                "anthropic-version": "2023-06-01",
                "anthropic-beta": "experimental-cc-routine-2026-04-01",
                "Content-Type": "application/json",
            },
            json={"text": texto},
            timeout=20,
        )
        logger.info(f"[chat] fire -> HTTP {r.status_code}")
        return {"ok": r.status_code < 300, "status": r.status_code,
                "body": r.text[:300], "fire_url_tail": fire_url[-10:]}
    except Exception as e:
        logger.warning(f"[chat] fire excepción: {e}")
        return {"ok": False, "motivo": "excepcion", "error": str(e)}

ETAPAS_ABIERTAS = [EtapaOportunidad.lead, EtapaOportunidad.contactado,
                   EtapaOportunidad.propuesta, EtapaOportunidad.negociacion]

# Campos que nunca se actualizan desde el payload (anti mass-assignment).
CAMPOS_PROHIBIDOS = {"id", "created_by", "created_at", "updated_at", "user_id",
                     "external_id", "fuente", "proyecto_id"}

# Estados válidos para una acción del chat (anti valores arbitrarios).
ESTADOS_CHAT_VALIDOS = {"aprobado", "rechazado", "esperando", "info"}


# ── CRUD (autenticado con JWT) ────────────────────────────────────────────────

@router.get("/oportunidades", response_model=List[OportunidadOut])
def listar(db: Session = Depends(get_db), _=Depends(get_db_user)):
    return (db.query(Oportunidad)
              .order_by(Oportunidad.etapa, Oportunidad.orden, Oportunidad.created_at.desc())
              .all())


@router.post("/oportunidades", response_model=OportunidadOut)
def crear(data: OportunidadCreate, db: Session = Depends(get_db), _=Depends(require_editor)):
    # nueva oportunidad va al fondo de su columna
    base = db.query(Oportunidad).filter_by(etapa=data.etapa).count()
    op = Oportunidad(**data.model_dump(), orden=base)
    db.add(op)
    db.commit()
    db.refresh(op)
    return op


@router.get("/oportunidades/{oid}", response_model=OportunidadOut)
def detalle(oid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    op = db.query(Oportunidad).filter_by(id=oid).first()
    if not op:
        raise HTTPException(404, "Oportunidad no encontrada")
    return op


@router.patch("/oportunidades/{oid}", response_model=OportunidadOut)
def editar(oid: int, data: OportunidadUpdate, db: Session = Depends(get_db),
           _=Depends(require_editor)):
    op = db.query(Oportunidad).filter_by(id=oid).first()
    if not op:
        raise HTTPException(404, "Oportunidad no encontrada")
    for k, v in data.model_dump(exclude_unset=True).items():
        if k in CAMPOS_PROHIBIDOS:
            continue
        setattr(op, k, v)
    db.commit()
    db.refresh(op)
    return op


@router.delete("/oportunidades/{oid}")
def eliminar(oid: int, db: Session = Depends(get_db),
             current_user: User = Depends(get_db_user)):
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(403, "Sin permisos")
    op = db.query(Oportunidad).filter_by(id=oid).first()
    if not op:
        raise HTTPException(404, "Oportunidad no encontrada")
    db.delete(op)
    db.commit()
    return {"ok": True}


@router.post("/oportunidades/{oid}/convertir", response_model=ProyectoOut)
def convertir_a_proyecto(oid: int, db: Session = Depends(get_db),
                         current_user: User = Depends(get_db_user)):
    """Convierte una oportunidad ganada en un Proyecto y las deja vinculadas."""
    op = db.query(Oportunidad).filter_by(id=oid).first()
    if not op:
        raise HTTPException(404, "Oportunidad no encontrada")
    if op.proyecto_id:
        raise HTTPException(400, "La oportunidad ya está vinculada a un proyecto.")

    p = Proyecto(
        nombre=op.titulo,
        cliente=op.empresa,
        descripcion=op.descripcion,
        status=ProyectoStatus.planificacion,
        created_by=current_user.id,
    )
    db.add(p)
    db.flush()                       # obtener p.id sin segundo commit
    op.proyecto_id = p.id
    op.etapa = EtapaOportunidad.ganado
    db.commit()
    db.refresh(p)
    # _enrich vive en proyectos.py; acá devolvemos los campos calculados en cero.
    # Construimos el dict desde las columnas reales (no p.__dict__, que arrastra
    # _sa_instance_state).
    data = {c.name: getattr(p, c.name) for c in p.__table__.columns}
    return {
        **data,
        "progreso": 0.0, "total_tareas": 0, "tareas_completadas": 0,
        "total_puntos": 0, "puntos_completados": 0,
    }


@router.get("/stats", response_model=CRMStats)
def stats(db: Session = Depends(get_db), _=Depends(get_db_user)):
    ops = db.query(Oportunidad).all()
    por_etapa = {e.value: {"count": 0, "valor": 0.0} for e in EtapaOportunidad}
    valor_pipeline = valor_ganado = 0.0
    ganadas = perdidas = 0
    for op in ops:
        cell = por_etapa[op.etapa.value]
        cell["count"] += 1
        cell["valor"] += op.valor_estimado or 0.0
        if op.etapa in ETAPAS_ABIERTAS:
            valor_pipeline += op.valor_estimado or 0.0
        elif op.etapa == EtapaOportunidad.ganado:
            valor_ganado += op.valor_estimado or 0.0
            ganadas += 1
        elif op.etapa == EtapaOportunidad.perdido:
            perdidas += 1
    return CRMStats(
        total_oportunidades=len(ops),
        valor_pipeline=round(valor_pipeline, 2),
        valor_ganado=round(valor_ganado, 2),
        ganadas=ganadas,
        perdidas=perdidas,
        por_etapa=por_etapa,
    )


# ── Endpoint EXTERNO (API Key) ────────────────────────────────────────────────
# Permite a sistemas externos (n8n, formularios web, scripts) crear o actualizar
# oportunidades de forma idempotente usando `external_id`.

@router.post("/external/oportunidades", response_model=OportunidadOut,
             tags=["crm-external"])
def upsert_externo(data: OportunidadExternal, db: Session = Depends(get_db),
                   _=Depends(verify_api_key)):
    def _aplicar_update(op):
        for k, v in data.model_dump(exclude_unset=True).items():
            if k in CAMPOS_PROHIBIDOS:       # external_id ya coincide; no se reescribe
                continue
            setattr(op, k, v)

    op = db.query(Oportunidad).filter_by(external_id=data.external_id).first()
    if op:                                   # UPDATE
        _aplicar_update(op)
        db.commit()
        db.refresh(op)
        return op

    # CREATE — protegido contra carrera: si otro request insertó el mismo external_id
    # entre el SELECT y el INSERT, capturamos el IntegrityError y caemos al UPDATE.
    payload = data.model_dump(exclude_unset=True)
    etapa = payload.pop("etapa", None) or EtapaOportunidad.lead
    base = db.query(Oportunidad).filter_by(etapa=etapa).count()
    op = Oportunidad(
        titulo=payload.pop("titulo", None) or payload["empresa"],
        etapa=etapa,
        fuente=FuenteOportunidad.api,
        orden=base,
        **payload,
    )
    db.add(op)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        op = db.query(Oportunidad).filter_by(external_id=data.external_id).first()
        if not op:
            raise HTTPException(409, "Conflicto al crear la oportunidad.")
        _aplicar_update(op)
        db.commit()
    db.refresh(op)
    return op


# ── Disparo manual del outreach en código (envío / escucha) ───────────────────
# Útil para testear sin esperar al scheduler. Protegidos con JWT (uso interno).

@router.post("/outreach/enviar")
def disparar_envio(db: Session = Depends(get_db), current_user: User = Depends(get_db_user)):
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(403, "Sin permisos")
    from app.outreach_service import enviar_pendientes
    enviados = enviar_pendientes(db)
    return {"enviados": enviados}


@router.post("/outreach/revisar-inbox")
def disparar_inbox(db: Session = Depends(get_db), current_user: User = Depends(get_db_user)):
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(403, "Sin permisos")
    from app.outreach_service import revisar_inbox
    registradas = revisar_inbox(db)
    return {"registradas": registradas}


@router.get("/outreach/config-check")
def config_check(current_user: User = Depends(get_db_user)):
    """Chequea las env del disparo de chat SIN exponer secretos: si están seteadas, su largo,
    si son 100% ASCII (un '—' u otro char raro pegado las rompe), y la cola de las URLs."""
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(403, "Sin permisos")
    def info(name, mostrar_cola=False):
        v = os.getenv(name, "")
        return {"set": bool(v), "len": len(v), "ascii_ok": v.isascii(),
                "cola": (v[-10:] if mostrar_cola and v else None)}
    return {
        "CLAUDE_ROUTINE_FIRE_URL": info("CLAUDE_ROUTINE_FIRE_URL", mostrar_cola=True),
        "CLAUDE_ROUTINE_TOKEN": info("CLAUDE_ROUTINE_TOKEN"),
        "SELF_API_BASE": info("SELF_API_BASE", mostrar_cola=True),
        "EXTERNAL_API_KEY": info("EXTERNAL_API_KEY"),
    }


@router.post("/outreach/test-fire")
def test_fire_chat(current_user: User = Depends(get_db_user)):
    """Diagnóstico: dispara la routine chat-responder y devuelve QUÉ respondió el /fire.
    Sirve para verificar las env CLAUDE_ROUTINE_*/SELF_API_BASE sin mirar logs."""
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(403, "Sin permisos")
    return _fire_chat_responder("PRUEBA DIAGNOSTICO: confirmá en una línea que el disparo automático anda.")


@router.get("/external/stats", response_model=CRMStats, tags=["crm-external"])
def stats_externo(db: Session = Depends(get_db), _=Depends(verify_api_key)):
    """Stats del pipeline para los agentes en la nube (API key). Misma data que /stats (JWT)."""
    return stats(db=db, _=None)


@router.get("/external/contactos/resumen", tags=["crm-external"])
def contactos_resumen(db: Session = Depends(get_db), _=Depends(verify_api_key)):
    """Resumen de Contactos por estado, para el ciclo comercial autónomo (API key)."""
    from sqlalchemy import func as _func
    filas = (db.query(Contacto.estado, _func.count(Contacto.id))
               .group_by(Contacto.estado).all())
    return {"por_estado": {estado: cant for estado, cant in filas},
            "total": sum(c for _, c in filas)}


@router.get("/external/outbox", response_model=List[OportunidadOut], tags=["crm-external"])
def outbox(db: Session = Depends(get_db), _=Depends(verify_api_key)):
    """Leads con email YA escrito y pendientes de envío. Lo consume n8n para disparar
    los correos. Devuelve solo los que tienen contacto_email y outreach_status='escrito'."""
    return (db.query(Oportunidad)
              .filter(Oportunidad.outreach_status == "escrito",
                      Oportunidad.contacto_email.isnot(None))
              .order_by(Oportunidad.created_at)
              .all())


def _promover_contacto(c: Contacto, db: Session) -> Oportunidad:
    """Sube un contacto al pipeline creando una Oportunidad (etapa 'contactado').
    Si ya estaba promovido, devuelve la oportunidad existente."""
    if c.oportunidad_id:
        return db.query(Oportunidad).filter_by(id=c.oportunidad_id).first()
    base = db.query(Oportunidad).filter_by(etapa=EtapaOportunidad.contactado).count()
    op = Oportunidad(
        empresa=c.empresa,
        titulo=f"{c.empresa} — respondió",
        contacto_nombre=c.nombre,
        contacto_email=c.email,
        contacto_telefono=c.telefono,
        descripcion=c.info,
        etapa=EtapaOportunidad.contactado,
        fuente=FuenteOportunidad.api,
        orden=base,
        idioma=c.idioma,
        disparador=c.disparador,
        mensaje_asunto=c.mensaje_asunto,
        mensaje_cuerpo=c.mensaje_cuerpo,
        outreach_status="respondido",
        respuesta_recibida=c.respuesta_recibida,
    )
    db.add(op)
    db.flush()
    c.oportunidad_id = op.id
    return op


@router.post("/external/respuesta", tags=["crm-external"])
def registrar_respuesta(data: RespuestaInbound, db: Session = Depends(get_db),
                        _=Depends(verify_api_key)):
    """Registra la respuesta de un lead (la trae n8n desde el inbox). Matchea el CONTACTO
    por email (el más reciente), marca estado='respondido', guarda el texto y lo PROMUEVE
    al pipeline (crea una Oportunidad en etapa 'contactado'). Si no hay contacto, cae al
    matcheo histórico por Oportunidad (compatibilidad)."""
    email = (data.email or "").strip().lower()
    c = (db.query(Contacto)
           .filter(func.lower(Contacto.email) == email)
           .order_by(Contacto.created_at.desc())
           .first())
    if c:
        c.respuesta_recibida = data.texto
        c.estado = "respondido"
        op = _promover_contacto(c, db)
        db.commit()
        return {"matched": True, "contacto_id": c.id, "empresa": c.empresa,
                "promovido": True, "oportunidad_id": op.id if op else None}

    # Fallback histórico: leads que ya estaban directo en el pipeline.
    op = (db.query(Oportunidad)
            .filter(func.lower(Oportunidad.contacto_email) == email)
            .order_by(Oportunidad.created_at.desc())
            .first())
    if not op:
        return {"matched": False}
    op.respuesta_recibida = data.texto
    op.outreach_status = "respondido"
    if op.etapa == EtapaOportunidad.lead:
        op.etapa = EtapaOportunidad.contactado
    db.commit()
    return {"matched": True, "id": op.id, "empresa": op.empresa, "promovido": False}


# ── Contactos (base de prospección) ───────────────────────────────────────────
# Los agentes SDR dejan acá los leads que encuentran/contactan. Solo suben al
# pipeline (Oportunidad) cuando responden. Los contactados sin respuesta quedan
# acá con estado='contactado'.

@router.get("/contactos", response_model=List[ContactoOut])
def listar_contactos(estado: Optional[str] = None, origen: Optional[str] = None,
                     db: Session = Depends(get_db), _=Depends(get_db_user)):
    q = db.query(Contacto)
    if estado:
        q = q.filter(Contacto.estado == estado)
    if origen:
        q = q.filter(Contacto.origen == origen)
    return q.order_by(Contacto.created_at.desc()).all()


@router.post("/contactos", response_model=ContactoOut)
def crear_contacto(data: ContactoCreate, db: Session = Depends(get_db), _=Depends(require_editor)):
    c = Contacto(**data.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c


@router.patch("/contactos/{cid}", response_model=ContactoOut)
def editar_contacto(cid: int, data: ContactoUpdate, db: Session = Depends(get_db),
                    _=Depends(require_editor)):
    c = db.query(Contacto).filter_by(id=cid).first()
    if not c:
        raise HTTPException(404, "Contacto no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    db.commit(); db.refresh(c)
    return c


@router.post("/contactos/{cid}/promover", response_model=OportunidadOut)
def promover_contacto_manual(cid: int, db: Session = Depends(get_db), _=Depends(require_editor)):
    """Sube manualmente un contacto al pipeline (sin esperar respuesta)."""
    c = db.query(Contacto).filter_by(id=cid).first()
    if not c:
        raise HTTPException(404, "Contacto no encontrado")
    op = _promover_contacto(c, db)
    if c.estado not in ("respondido",):
        c.estado = "respondido"
    db.commit(); db.refresh(op)
    return op


@router.delete("/contactos/{cid}")
def eliminar_contacto(cid: int, db: Session = Depends(get_db),
                      current_user: User = Depends(get_db_user)):
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(403, "Sin permisos")
    c = db.query(Contacto).filter_by(id=cid).first()
    if not c:
        raise HTTPException(404, "Contacto no encontrado")
    db.delete(c); db.commit()
    return {"ok": True}


@router.post("/external/contactos", response_model=ContactoOut, tags=["crm-external"])
def upsert_contacto_externo(data: ContactoExternal, db: Session = Depends(get_db),
                            _=Depends(verify_api_key)):
    """El agente SDR deja/actualiza un lead en la base de prospección. Upsert idempotente
    por external_id. NO entra al pipeline: vive en Contactos hasta que responda."""
    c = db.query(Contacto).filter_by(external_id=data.external_id).first()
    payload = data.model_dump(exclude_unset=True)
    if c:
        for k, v in payload.items():
            if k == "external_id":
                continue
            setattr(c, k, v)
        db.commit(); db.refresh(c)
        return c
    c = Contacto(origen=payload.pop("origen", None) or "Agente SDR", **payload)
    db.add(c)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        c = db.query(Contacto).filter_by(external_id=data.external_id).first()
        if not c:
            raise HTTPException(409, "Conflicto al crear el contacto.")
    db.refresh(c)
    return c


@router.get("/external/contactos/outbox", response_model=List[ContactoOut], tags=["crm-external"])
def contactos_outbox(db: Session = Depends(get_db), _=Depends(verify_api_key)):
    """Contactos con el mensaje YA escrito, pendientes de envío (estado='escrito').
    Lo consume n8n para disparar el primer contacto."""
    return (db.query(Contacto)
              .filter(Contacto.estado == "escrito", Contacto.email.isnot(None))
              .order_by(Contacto.created_at)
              .all())


# ── Cola de búsqueda (Lead Jobs) ──────────────────────────────────────────────
# La plataforma encola pedidos (JWT); el Equipo de Venta y Prospección los
# consume por polling (API Key) y devuelve los leads vía /external/contactos.

@router.post("/lead-jobs", response_model=LeadJobOut)
def crear_lead_job(data: LeadJobCreate, db: Session = Depends(get_db),
                   _=Depends(require_editor)):
    job = LeadJob(icp=data.icp, cantidad=data.cantidad, fundamento=data.fundamento)
    db.add(job); db.commit(); db.refresh(job)
    return job


@router.get("/lead-jobs", response_model=List[LeadJobOut])
def listar_lead_jobs(db: Session = Depends(get_db), _=Depends(get_db_user)):
    return db.query(LeadJob).order_by(LeadJob.created_at.desc()).all()


@router.get("/lead-jobs/pending", response_model=List[LeadJobOut], tags=["crm-external"])
def lead_jobs_pendientes(db: Session = Depends(get_db), _=Depends(verify_api_key)):
    return (db.query(LeadJob).filter_by(status="pendiente")
              .order_by(LeadJob.created_at).all())


@router.patch("/lead-jobs/{jid}", response_model=LeadJobOut, tags=["crm-external"])
def actualizar_lead_job(jid: int, data: LeadJobUpdate, db: Session = Depends(get_db),
                        _=Depends(verify_api_key)):
    job = db.query(LeadJob).filter_by(id=jid).first()
    if not job:
        raise HTTPException(404, "Lead job no encontrado")
    if data.status is not None:
        job.status = data.status
        if data.status in ("completado", "error"):
            job.processed_at = datetime.now(timezone.utc)
    if data.resumen is not None:
        job.resumen = data.resumen
    db.commit(); db.refresh(job)
    return job


# ── Chat persistente (humano ↔ orquestador) ───────────────────────────────────

@router.get("/chat", response_model=List[ChatMensajeOut])
def listar_chat(db: Session = Depends(get_db), _=Depends(get_db_user)):
    return db.query(ChatMensaje).order_by(ChatMensaje.created_at).all()


@router.post("/chat", response_model=ChatMensajeOut)
def postear_humano(data: ChatMensajeCreate, background_tasks: BackgroundTasks,
                   db: Session = Depends(get_db), _=Depends(require_editor)):
    msg = ChatMensaje(rol="humano", contenido=data.contenido)
    db.add(msg); db.commit(); db.refresh(msg)
    # Dispara al orquestador (routine en el plan) para que responda este mensaje.
    background_tasks.add_task(_fire_chat_responder, data.contenido)
    return msg


@router.patch("/chat/{mid}/estado", response_model=ChatMensajeOut)
def set_estado_chat(mid: int, estado: str, db: Session = Depends(get_db),
                    _=Depends(require_manager)):
    """El humano aprueba/rechaza una acción propuesta por el agente."""
    if estado not in ESTADOS_CHAT_VALIDOS:
        raise HTTPException(422, f"Estado inválido. Permitidos: {sorted(ESTADOS_CHAT_VALIDOS)}")
    msg = db.query(ChatMensaje).filter_by(id=mid).first()
    if not msg:
        raise HTTPException(404, "Mensaje no encontrado")
    msg.estado = estado                      # aprobado / rechazado
    db.commit(); db.refresh(msg)
    return msg


@router.get("/external/chat", response_model=List[ChatMensajeOut], tags=["crm-external"])
def listar_chat_externo(limit: int = 50, db: Session = Depends(get_db),
                        _=Depends(verify_api_key)):
    """Lo consume el 'puente' (Claude Code en loop, sobre el plan) para leer el chat sin login JWT.
    Devuelve los últimos `limit` mensajes en orden cronológico. El puente detecta los mensajes
    humanos que aún no tienen respuesta del agente y los contesta vía POST /external/chat."""
    msgs = (db.query(ChatMensaje)
              .order_by(ChatMensaje.created_at.desc())
              .limit(limit)
              .all())
    return list(reversed(msgs))


@router.post("/external/chat", response_model=ChatMensajeOut, tags=["crm-external"])
def postear_agente(data: ChatMensajeCreate, db: Session = Depends(get_db),
                   _=Depends(verify_api_key)):
    msg = ChatMensaje(
        rol="agente",
        contenido=data.contenido,
        requiere_aprobacion=data.requiere_aprobacion,
        estado="esperando" if data.requiere_aprobacion else "info",
    )
    db.add(msg); db.commit(); db.refresh(msg)
    return msg


# ── Aviso por mail a los dos correos del funnel ───────────────────────────────

@router.post("/external/notify", tags=["crm-external"])
def notificar_funnel(data: FunnelNotify, _=Depends(verify_api_key)):
    from app.email_service import enviar_aviso_funnel
    res = enviar_aviso_funnel(
        asunto=data.asunto, titulo=data.titulo,
        subtitulo=data.subtitulo or "", cuerpo_html=data.cuerpo,
        prioridad=data.prioridad or "info",
    )
    return {
        "enviados": [e for e, err in res.items() if err is None],
        "fallidos": {e: err for e, err in res.items() if err is not None},
    }
