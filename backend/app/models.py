from datetime import datetime, date
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
    created_at = Column(DateTime, default=datetime.utcnow)

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
    created_at = Column(DateTime, default=datetime.utcnow)

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
    created_at = Column(DateTime, default=datetime.utcnow)

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
    created_at = Column(DateTime, default=datetime.utcnow)

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
    created_at = Column(DateTime, default=datetime.utcnow)

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
    created_at = Column(DateTime, default=datetime.utcnow)

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

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    proyecto = relationship("Proyecto", foreign_keys=[proyecto_id])


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
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)


class ChatMensaje(Base):
    """Chat persistente entre el humano y el orquestador del equipo. Siempre visible.
    El agente escribe vía API key; el humano vía JWT. Las aprobaciones pausan acciones."""
    __tablename__ = "chat_mensajes"

    id = Column(Integer, primary_key=True)
    rol = Column(String, nullable=False)               # agente/humano/sistema
    contenido = Column(Text, nullable=False)
    requiere_aprobacion = Column(Boolean, default=False)
    estado = Column(String, default="info")            # info/esperando/aprobado/rechazado
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


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
    created_at = Column(DateTime, default=datetime.utcnow)

    proyecto = relationship("Proyecto", back_populates="requerimiento")
