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
