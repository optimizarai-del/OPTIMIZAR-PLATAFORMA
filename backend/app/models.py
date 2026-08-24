from datetime import datetime, date, timezone


def _utcnow():
    """Reemplazo de datetime.utcnow (deprecado): UTC aware, apto para defaults de SQLAlchemy."""
    return datetime.now(timezone.utc)
from enum import Enum
from sqlalchemy import (Column, Integer, String, DateTime, Date, Boolean,
                        Float, Text, ForeignKey, Enum as SQLEnum, JSON)
from sqlalchemy.orm import relationship
from app.database import Base


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    developer = "developer"
    viewer = "viewer"


class ProyectoStatus(str, Enum):
    planificacion = "planificacion"
    en_progreso = "en_progreso"
    pausado = "pausado"
    completado = "completado"


class TareaStatus(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    revision = "revision"
    completada = "completada"
    bloqueada = "bloqueada"


class TareaPrioridad(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    urgente = "urgente"


class TipoRegistro(str, Enum):
    timer = "timer"
    manual = "manual"


class RequerimientoStatus(str, Enum):
    nuevo = "nuevo"
    evaluacion = "evaluacion"
    aprobado = "aprobado"
    rechazado = "rechazado"
    convertido = "convertido"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.developer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)

    tareas_asignadas = relationship("Tarea", back_populates="asignado", foreign_keys="Tarea.asignado_a")
    registros = relationship("RegistroTiempo", back_populates="user")


class Proyecto(Base):
    __tablename__ = "proyectos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    cliente = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    status = Column(SQLEnum(ProyectoStatus), default=ProyectoStatus.planificacion)
    color = Column(String, default="#6366F1")
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=_utcnow)

    github_repo = Column(String, nullable=True)
    github_last_sync = Column(DateTime, nullable=True)
    github_last_commit_sha = Column(String, nullable=True)

    tareas = relationship("Tarea", back_populates="proyecto", cascade="all, delete-orphan")
    puntos_accion = relationship("PuntoAccion", back_populates="proyecto",
                                 cascade="all, delete-orphan", order_by="PuntoAccion.orden")
    requerimiento = relationship("Requerimiento", back_populates="proyecto", uselist=False)


class PuntoAccion(Base):
    __tablename__ = "puntos_accion"

    id = Column(Integer, primary_key=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    orden = Column(Integer, default=0)
    completado = Column(Boolean, default=False)
    created_at = Column(DateTime, default=_utcnow)

    proyecto = relationship("Proyecto", back_populates="puntos_accion")


class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=False)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    status = Column(SQLEnum(TareaStatus), default=TareaStatus.pendiente)
    prioridad = Column(SQLEnum(TareaPrioridad), default=TareaPrioridad.media)
    asignado_a = Column(Integer, ForeignKey("users.id"), nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin_estimada = Column(Date, nullable=True)
    fecha_fin_real = Column(Date, nullable=True)
    minutos_estimados = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=_utcnow)

    proyecto = relationship("Proyecto", back_populates="tareas")
    asignado = relationship("User", back_populates="tareas_asignadas", foreign_keys=[asignado_a])
    registros = relationship("RegistroTiempo", back_populates="tarea", cascade="all, delete-orphan")


class RegistroTiempo(Base):
    __tablename__ = "registros_tiempo"

    id = Column(Integer, primary_key=True)
    tarea_id = Column(Integer, ForeignKey("tareas.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    minutos = Column(Integer, nullable=False)
    descripcion = Column(Text, nullable=True)
    resultado = Column(Text, nullable=True)
    tipo = Column(SQLEnum(TipoRegistro), default=TipoRegistro.manual)
    fecha = Column(Date, default=date.today)
    created_at = Column(DateTime, default=_utcnow)

    tarea = relationship("Tarea", back_populates="registros")
    user = relationship("User", back_populates="registros")


class NotificacionTipo(str, Enum):
    tarea_asignada      = "tarea_asignada"
    cambio_estado       = "cambio_estado"
    reasignacion        = "reasignacion"
    detalles_actualizados = "detalles_actualizados"
    tarea_completada    = "tarea_completada"


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True)
    tipo = Column(SQLEnum(NotificacionTipo), nullable=False)
    destinatario_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    destinatario_email = Column(String, nullable=False)
    tarea_id = Column(Integer, ForeignKey("tareas.id"), nullable=True)
    asunto = Column(String, nullable=False)
    cuerpo_html = Column(Text, nullable=True)
    enviado = Column(Boolean, default=False)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_utcnow)

    destinatario = relationship("User", foreign_keys=[destinatario_id])
    tarea = relationship("Tarea", foreign_keys=[tarea_id])


class EtapaOportunidad(str, Enum):
    lead          = "lead"
    contactado    = "contactado"
    propuesta     = "propuesta"
    negociacion   = "negociacion"
    ganado        = "ganado"
    perdido       = "perdido"


class FuenteOportunidad(str, Enum):
    manual    = "manual"
    web       = "web"
    referido  = "referido"
    api       = "api"          # creada/actualizada vía endpoint externo
    otro      = "otro"


class Oportunidad(Base):
    """Oportunidad de venta del pipeline CRM. La info de contacto va embebida
    (no hay entidad Contacto separada, por decisión de alcance)."""
    __tablename__ = "oportunidades"

    id = Column(Integer, primary_key=True)

    # ── Contacto embebido ──
    empresa = Column(String, nullable=False)
    contacto_nombre = Column(String, nullable=True)
    contacto_email = Column(String, nullable=True, index=True)
    contacto_telefono = Column(String, nullable=True)

    # ── Pipeline ──
    titulo = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    etapa = Column(SQLEnum(EtapaOportunidad), default=EtapaOportunidad.lead, index=True)
    valor_estimado = Column(Float, default=0.0)        # monto potencial
    probabilidad = Column(Integer, default=0)          # 0-100 %
    orden = Column(Integer, default=0)                 # orden dentro de la columna
    fuente = Column(SQLEnum(FuenteOportunidad), default=FuenteOportunidad.manual)

    # ── Clave de idempotencia para el endpoint externo (upsert) ──
    external_id = Column(String, nullable=True, unique=True, index=True)

    responsable = Column(String, nullable=True)
    proxima_accion = Column(String, nullable=True)
    fecha_cierre_estimada = Column(Date, nullable=True)

    # ── Outreach del Equipo de Venta y Prospección (columnas aditivas, nullable) ──
    idioma = Column(String, nullable=True)             # idioma del lead (es, en, pt...)
    disparador = Column(Text, nullable=True)           # razón concreta de contacto
    mensaje_asunto = Column(String, nullable=True)     # asunto del email escrito
    mensaje_cuerpo = Column(Text, nullable=True)       # cuerpo del email escrito
    outreach_status = Column(String, default="sin_contactar")  # sin_contactar/escrito/enviado/respondido/rebote/baja
    respuesta_recibida = Column(Text, nullable=True)   # texto de la respuesta del lead

    # ── Conversión a proyecto (cuando se gana) ──
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=True)

    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    proyecto = relationship("Proyecto", foreign_keys=[proyecto_id])


class Contacto(Base):
    """Base de prospección. Los agentes (SDR) dejan acá los leads que encuentran y contactan.
    NO es el pipeline de ventas: un contacto sube a Oportunidad (pipeline) SOLO cuando responde
    el primer contacto. Los contactados sin respuesta quedan acá con estado='contactado'."""
    __tablename__ = "contactos"

    id = Column(Integer, primary_key=True)

    # ── Identidad / info ──
    empresa = Column(String, nullable=False)
    nombre = Column(String, nullable=True)
    email = Column(String, nullable=True, index=True)
    telefono = Column(String, nullable=True)
    info = Column(Text, nullable=True)                 # contexto/descripción del lead

    # ── Etiqueta de origen (de dónde viene) ──
    origen = Column(String, default="agente", index=True)  # ej: "Agente SDR", "manual", vertical/campaña

    # ── Outreach ──
    idioma = Column(String, nullable=True)
    disparador = Column(Text, nullable=True)           # razón concreta del contacto
    mensaje_asunto = Column(String, nullable=True)
    mensaje_cuerpo = Column(Text, nullable=True)
    respuesta_recibida = Column(Text, nullable=True)

    # estado: nuevo / escrito / contactado / respondido / rebote / baja
    estado = Column(String, default="nuevo", index=True)

    # ── Idempotencia (upsert del agente) ──
    external_id = Column(String, nullable=True, unique=True, index=True)

    # ── Promoción al pipeline (cuando responde) ──
    oportunidad_id = Column(Integer, ForeignKey("oportunidades.id"), nullable=True)

    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    oportunidad = relationship("Oportunidad", foreign_keys=[oportunidad_id])


class LeadJob(Base):
    """Pedido de búsqueda de leads encolado desde la plataforma. Lo consume el
    Equipo de Venta y Prospección (Claude Code) por polling y devuelve los leads
    vía el endpoint externo del CRM. Patrón de polling invertido — sin API de Anthropic."""
    __tablename__ = "lead_jobs"

    id = Column(Integer, primary_key=True)
    icp = Column(JSON, default=dict)                   # rubro, tamaño, cargo, geografía, idiomas
    cantidad = Column(Integer, default=20)             # cupo de leads para esta corrida
    status = Column(String, default="pendiente", index=True)  # pendiente/procesando/completado/error
    fundamento = Column(Text, nullable=True)           # por qué el COO eligió este segmento
    resumen = Column(Text, nullable=True)              # resultado de la corrida
    created_at = Column(DateTime, default=_utcnow)
    processed_at = Column(DateTime, nullable=True)


class ChatMensaje(Base):
    """Chat persistente entre el humano y el orquestador del equipo. Siempre visible.
    El agente escribe vía API key; el humano vía JWT. Las aprobaciones pausan acciones.

    `canal` separa conversaciones por orquestador: 'crm' (funnel de ventas, default
    histórico) y 'agentes' (centro de comando de marketing/general). Aditivo y nullable."""
    __tablename__ = "chat_mensajes"

    id = Column(Integer, primary_key=True)
    canal = Column(String, default="crm", index=True)  # crm / agentes
    rol = Column(String, nullable=False)               # agente/humano/sistema
    contenido = Column(Text, nullable=False)
    requiere_aprobacion = Column(Boolean, default=False)
    estado = Column(String, default="info")            # info/esperando/aprobado/rechazado
    created_at = Column(DateTime, default=_utcnow, index=True)


class AgenteTarea(Base):
    """Tarea que el orquestador le encarga a un subagente especializado. La plataforma
    la encola; el subagente (Claude Code sobre el plan) la consume por polling con API key,
    la ejecuta usando sus MCPs y devuelve el resultado. Patrón de polling invertido.

    Implementa los roles del documento VIVE: investigacion, contenido, creativo, sdr,
    calificacion, crm, ads."""
    __tablename__ = "agente_tareas"

    id = Column(Integer, primary_key=True)
    agente = Column(String, nullable=False, index=True)   # investigacion/contenido/creativo/sdr/calificacion/crm/ads
    instruccion = Column(Text, nullable=False)             # qué pidió el orquestador
    contexto = Column(JSON, default=dict)                  # datos extra (ids, params)
    estado = Column(String, default="pendiente", index=True)  # pendiente/en_proceso/completado/error/requiere_aprobacion
    resultado = Column(Text, nullable=True)               # salida del subagente
    origen = Column(String, default="orquestador")        # orquestador/humano
    prioridad = Column(String, default="media")           # alta/media/baja
    created_at = Column(DateTime, default=_utcnow, index=True)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)
    processed_at = Column(DateTime, nullable=True)


class AnalisisEstado(str, Enum):
    pendiente = "pendiente"      # todavía no se analizó
    cubierto = "cubierto"        # un servicio existente cubre el requerimiento
    no_cubierto = "no_cubierto"  # ningún servicio lo cubre → consultar con desarrollo
    error = "error"              # falló el análisis


class Requerimiento(Base):
    __tablename__ = "requerimientos"

    id = Column(Integer, primary_key=True)
    nombre_cliente = Column(String, nullable=False)
    sector = Column(String, nullable=True)
    personas_reunion = Column(Text, nullable=True)
    sistemas_core = Column(Text, nullable=True)
    herramientas = Column(JSON, default=list)
    uso_ia = Column(Text, nullable=True)
    tipos_acceso = Column(JSON, default=list)
    estado_bd = Column(Text, nullable=True)
    nombre_proceso = Column(String, nullable=True)
    trigger_proceso = Column(Text, nullable=True)
    pasos_manuales = Column(Text, nullable=True)
    volumen_proceso = Column(String, nullable=True)
    tiempo_por_proceso = Column(String, nullable=True)
    responsable_comercial = Column(String, nullable=True)
    fecha_entrega = Column(Date, nullable=True)
    status = Column(SQLEnum(RequerimientoStatus), default=RequerimientoStatus.nuevo)
    proyecto_id = Column(Integer, ForeignKey("proyectos.id"), nullable=True)
    created_at = Column(DateTime, default=_utcnow)

    # ── Análisis IA: matching contra el catálogo "Nuestros Servicios" ──
    # Se corre automático al crear el requerimiento (ver routers/requerimientos.py).
    analisis_estado = Column(String, default=AnalisisEstado.pendiente.value, index=True)
    servicio_match_id = Column(Integer, ForeignKey("servicios.id"), nullable=True)
    analisis_justificacion = Column(Text, nullable=True)   # por qué (no) lo cubre
    analisis_confianza = Column(Integer, nullable=True)    # 0-100
    analisis_at = Column(DateTime, nullable=True)

    proyecto = relationship("Proyecto", back_populates="requerimiento")
    servicio_match = relationship("Servicio", foreign_keys=[servicio_match_id])


class Servicio(Base):
    """Catálogo editable de servicios que OPTIMIZAR puede ofrecer hoy.
    Se administra desde la sección "Nuestros Servicios" y la IA lo usa para
    decidir si un requerimiento nuevo puede cubrirse con algo ya construido."""
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    categoria = Column(String, nullable=True)              # ej: Agentes, Automatización, Dashboards
    descripcion = Column(Text, nullable=True)              # qué resuelve, en una o dos frases
    capacidades = Column(Text, nullable=True)              # qué hace concretamente (alimenta el match)
    base_referencia = Column(String, nullable=True)        # proyecto base reutilizable (ej: Larrañaga)
    activo = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)


# ── Marketing · Meta Ads ──────────────────────────────────────────────────────
# Los datos los empuja el agente analista (Claude Code + MCP de Meta Ads) sobre el
# plan, vía endpoints externos con API key. Patrón de polling invertido, sin API de Anthropic.

class AdCampaign(Base):
    """Campaña publicitaria sincronizada desde Meta Ads. Upsert idempotente por external_id."""
    __tablename__ = "ad_campaigns"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True, nullable=False)  # id de campaña en Meta
    plataforma = Column(String, default="meta", index=True)
    nombre = Column(String, nullable=False)
    estado = Column(String, default="ACTIVE", index=True)   # ACTIVE/PAUSED/ARCHIVED
    objetivo = Column(String, nullable=True)                # OUTCOME_LEADS, OUTCOME_SALES, etc.
    cuenta_id = Column(String, nullable=True, index=True)   # act_<id> de Meta
    cuenta_nombre = Column(String, nullable=True)
    presupuesto_diario = Column(Float, nullable=True)       # en moneda de la cuenta
    moneda = Column(String, default="ARS")
    ultima_sync = Column(DateTime, default=_utcnow)
    created_at = Column(DateTime, default=_utcnow)

    metricas = relationship("AdMetric", back_populates="campaign",
                            cascade="all, delete-orphan")
    recomendaciones = relationship("AdRecommendation", back_populates="campaign",
                                   cascade="all, delete-orphan")


class AdMetric(Base):
    """Métricas diarias de una campaña (una fila por campaña y fecha).
    Upsert idempotente por (campaign_id, fecha)."""
    __tablename__ = "ad_metrics"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("ad_campaigns.id"), index=True, nullable=False)
    fecha = Column(Date, nullable=False, index=True)
    impresiones = Column(Integer, default=0)
    alcance = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    gasto = Column(Float, default=0.0)
    ctr = Column(Float, default=0.0)            # %
    cpc = Column(Float, default=0.0)
    cpm = Column(Float, default=0.0)
    frecuencia = Column(Float, default=0.0)
    conversiones = Column(Float, default=0.0)
    valor_conversiones = Column(Float, default=0.0)
    costo_conversion = Column(Float, default=0.0)
    roas = Column(Float, default=0.0)
    created_at = Column(DateTime, default=_utcnow)

    campaign = relationship("AdCampaign", back_populates="metricas")


class AdRecommendation(Base):
    """Recomendación del agente analista sobre una campaña. Upsert por external_id."""
    __tablename__ = "ad_recommendations"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True, nullable=False)  # clave idempotente del agente
    campaign_id = Column(Integer, ForeignKey("ad_campaigns.id"), index=True, nullable=True)
    tipo = Column(String, default="ajuste", index=True)   # escalar/pausar/presupuesto/creativo/audiencia/ajuste
    severidad = Column(String, default="media")           # alta/media/baja
    titulo = Column(String, nullable=False)
    detalle = Column(Text, nullable=True)                 # análisis y fundamento
    accion_sugerida = Column(Text, nullable=True)         # qué hacer concretamente
    metricas_clave = Column(JSON, default=dict)           # snapshot que motivó la reco
    estado = Column(String, default="nueva", index=True)  # nueva/aplicada/descartada
    created_at = Column(DateTime, default=_utcnow, index=True)

    campaign = relationship("AdCampaign", back_populates="recomendaciones")


# ── Gero — asistente IA de atención al cliente en WhatsApp ────────────────────
# A diferencia de los agentes que corren sobre routines de Claude Code, Gero usa la
# API de Anthropic directo (excepción documentada, igual que ai_service.py) porque
# necesita responder en tiempo real al webhook de WhatsApp. Estas dos tablas le dan
# MEMORIA: una conversación por número de WhatsApp + el historial completo de mensajes.

class GeroConversacion(Base):
    """Una conversación de WhatsApp por contacto (identificado por su número wa_id).
    Guarda el vínculo con el Contacto del CRM y un resumen rodante para memoria larga."""
    __tablename__ = "gero_conversaciones"

    id = Column(Integer, primary_key=True)

    # ── Identidad del canal ──
    wa_id = Column(String, nullable=False, unique=True, index=True)  # número E.164 sin '+' (id de WhatsApp)
    telefono = Column(String, nullable=True)          # número tal como llegó (con '+')
    nombre_perfil = Column(String, nullable=True)     # nombre del perfil de WhatsApp

    # ── Vínculo con el CRM ──
    contacto_id = Column(Integer, ForeignKey("contactos.id"), nullable=True, index=True)

    # ── Estado de la charla ──
    estado = Column(String, default="activa", index=True)  # activa/pausada/handoff_humano/cerrada
    resumen = Column(Text, nullable=True)             # memoria larga: resumen rodante de la relación
    nivel_interes = Column(String, nullable=True)     # frio/tibio/caliente (última clasificación de Gero)
    ultima_actividad = Column(DateTime, default=_utcnow, index=True)

    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    contacto = relationship("Contacto", foreign_keys=[contacto_id])
    mensajes = relationship("GeroMensaje", back_populates="conversacion",
                            order_by="GeroMensaje.created_at",
                            cascade="all, delete-orphan")


class GeroMensaje(Base):
    """Cada turno de la conversación de WhatsApp. Es la memoria a corto plazo que se
    recarga en cada respuesta. `rol` sigue el formato de la API de Anthropic."""
    __tablename__ = "gero_mensajes"

    id = Column(Integer, primary_key=True)
    conversacion_id = Column(Integer, ForeignKey("gero_conversaciones.id"),
                             nullable=False, index=True)

    rol = Column(String, nullable=False)              # user / assistant
    contenido = Column(Text, nullable=False)          # texto del mensaje
    wa_message_id = Column(String, nullable=True, index=True)  # id de WhatsApp (idempotencia inbound)
    herramientas = Column(JSON, nullable=True)        # tool_use/tool_result de ese turno (traza)

    created_at = Column(DateTime, default=_utcnow, index=True)

    conversacion = relationship("GeroConversacion", back_populates="mensajes")
