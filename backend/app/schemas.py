from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
from app.models import (UserRole, ProyectoStatus, TareaStatus, TareaPrioridad,
                        TipoRegistro, RequerimientoStatus, NotificacionTipo,
                        EtapaOportunidad, FuenteOportunidad)


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"


# ── Users ─────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.developer


class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class UserOut(BaseModel):
    id: int
    nombre: str
    email: str
    role: UserRole
    is_active: bool
    # Optional para que una fila con created_at NULL (p.ej. cargada por SQL manual)
    # no rompa la serialización de la respuesta (evita 500 en el login).
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Proyecto ──────────────────────────────────────────────────────────────────

class ProyectoCreate(BaseModel):
    nombre: str
    cliente: str
    descripcion: Optional[str] = None
    color: str = "#6366F1"
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    cliente: Optional[str] = None
    descripcion: Optional[str] = None
    color: Optional[str] = None
    status: Optional[ProyectoStatus] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    github_repo: Optional[str] = None


class ProyectoOut(BaseModel):
    id: int
    nombre: str
    cliente: str
    descripcion: Optional[str]
    status: ProyectoStatus
    color: str
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    progreso: float = 0.0
    total_tareas: int = 0
    tareas_completadas: int = 0
    total_puntos: int = 0
    puntos_completados: int = 0
    github_repo: Optional[str] = None
    github_last_sync: Optional[datetime] = None
    github_last_commit_sha: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GitHubRepoSet(BaseModel):
    repo: str  # "owner/repo"


class GitHubSyncResult(BaseModel):
    commits_analizados: int
    task_updates: List[dict]
    plan_updates: List[dict]
    summary: str


# ── AI: generación de plan / tareas / desde documento ─────────────────────────

class AIDocumentRequest(BaseModel):
    # texto plano (markdown, texto pegado, etc.) — tope de 200k chars para no
    # reventar memoria ni el contexto del modelo de IA.
    contenido: str = Field(max_length=200_000)


class AIGenerationResult(BaseModel):
    plan_creados: int = 0
    tareas_creadas: int = 0
    summary: str
    plan: List[dict] = []
    tareas: List[dict] = []


# ── PuntoAccion ───────────────────────────────────────────────────────────────

class PuntoAccionCreate(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    orden: int = 0


class PuntoAccionUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    orden: Optional[int] = None
    completado: Optional[bool] = None


class PuntoAccionOut(BaseModel):
    id: int
    proyecto_id: int
    titulo: str
    descripcion: Optional[str]
    orden: int
    completado: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Tarea ─────────────────────────────────────────────────────────────────────

class TareaCreate(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    proyecto_id: int
    asignado_a: Optional[int] = None
    prioridad: TareaPrioridad = TareaPrioridad.media
    fecha_inicio: Optional[date] = None
    fecha_fin_estimada: Optional[date] = None
    minutos_estimados: Optional[int] = Field(default=None, ge=0)


class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    status: Optional[TareaStatus] = None
    asignado_a: Optional[int] = None
    prioridad: Optional[TareaPrioridad] = None
    fecha_inicio: Optional[date] = None
    fecha_fin_estimada: Optional[date] = None
    fecha_fin_real: Optional[date] = None
    minutos_estimados: Optional[int] = Field(default=None, ge=0)


class TareaOut(BaseModel):
    id: int
    proyecto_id: int
    titulo: str
    descripcion: Optional[str]
    status: TareaStatus
    prioridad: TareaPrioridad
    asignado_a: Optional[int]
    asignado_nombre: Optional[str] = None
    fecha_inicio: Optional[date]
    fecha_fin_estimada: Optional[date]
    fecha_fin_real: Optional[date]
    minutos_estimados: Optional[int]
    minutos_trabajados: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── RegistroTiempo ────────────────────────────────────────────────────────────

class RegistroTiempoCreate(BaseModel):
    tarea_id: int
    minutos: int
    descripcion: Optional[str] = None
    resultado: Optional[str] = None
    tipo: TipoRegistro = TipoRegistro.manual
    fecha: date


class RegistroTiempoOut(BaseModel):
    id: int
    tarea_id: int
    user_id: int
    user_nombre: Optional[str] = None
    minutos: int
    descripcion: Optional[str]
    resultado: Optional[str]
    tipo: TipoRegistro
    fecha: date
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Requerimiento ─────────────────────────────────────────────────────────────

class RequerimientoCreate(BaseModel):
    nombre_cliente: str
    sector: Optional[str] = None
    personas_reunion: Optional[str] = None
    sistemas_core: Optional[str] = None
    herramientas: List[str] = []
    uso_ia: Optional[str] = None
    tipos_acceso: List[str] = []
    estado_bd: Optional[str] = None
    nombre_proceso: Optional[str] = None
    trigger_proceso: Optional[str] = None
    pasos_manuales: Optional[str] = None
    volumen_proceso: Optional[str] = None
    tiempo_por_proceso: Optional[str] = None
    responsable_comercial: Optional[str] = None
    fecha_entrega: Optional[date] = None


class RequerimientoUpdate(BaseModel):
    status: Optional[RequerimientoStatus] = None
    proyecto_id: Optional[int] = None
    nombre_cliente: Optional[str] = None
    sector: Optional[str] = None


class RequerimientoOut(BaseModel):
    id: int
    nombre_cliente: str
    sector: Optional[str]
    personas_reunion: Optional[str]
    sistemas_core: Optional[str]
    herramientas: List[str]
    uso_ia: Optional[str]
    tipos_acceso: List[str]
    estado_bd: Optional[str]
    nombre_proceso: Optional[str]
    trigger_proceso: Optional[str]
    pasos_manuales: Optional[str]
    volumen_proceso: Optional[str]
    tiempo_por_proceso: Optional[str]
    responsable_comercial: Optional[str]
    fecha_entrega: Optional[date]
    status: RequerimientoStatus
    proyecto_id: Optional[int]
    created_at: Optional[datetime] = None
    # ── Análisis IA contra el catálogo de servicios ──
    analisis_estado: str = "pendiente"
    servicio_match_id: Optional[int] = None
    servicio_match_nombre: Optional[str] = None   # lo completa el endpoint para la UI
    analisis_justificacion: Optional[str] = None
    analisis_confianza: Optional[int] = None
    analisis_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Servicios (catálogo "Nuestros Servicios") ─────────────────────────────────

class ServicioCreate(BaseModel):
    nombre: str = Field(min_length=1)
    categoria: Optional[str] = None
    descripcion: Optional[str] = None
    capacidades: Optional[str] = None
    base_referencia: Optional[str] = None
    activo: bool = True


class ServicioUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    descripcion: Optional[str] = None
    capacidades: Optional[str] = None
    base_referencia: Optional[str] = None
    activo: Optional[bool] = None


class ServicioOut(BaseModel):
    id: int
    nombre: str
    categoria: Optional[str]
    descripcion: Optional[str]
    capacidades: Optional[str]
    base_referencia: Optional[str]
    activo: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ── Notificaciones ───────────────────────────────────────────────────────────

class NotificacionOut(BaseModel):
    id: int
    tipo: NotificacionTipo
    destinatario_id: Optional[int]
    destinatario_email: str
    tarea_id: Optional[int]
    asunto: str
    enviado: bool
    error: Optional[str]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── CRM: Oportunidad ──────────────────────────────────────────────────────────

class OportunidadCreate(BaseModel):
    empresa: str
    titulo: str
    contacto_nombre: Optional[str] = None
    contacto_email: Optional[str] = None
    contacto_telefono: Optional[str] = None
    descripcion: Optional[str] = None
    etapa: EtapaOportunidad = EtapaOportunidad.lead
    valor_estimado: float = 0.0
    probabilidad: int = 0
    fuente: FuenteOportunidad = FuenteOportunidad.manual
    responsable: Optional[str] = None
    proxima_accion: Optional[str] = None
    fecha_cierre_estimada: Optional[date] = None


class OportunidadUpdate(BaseModel):
    empresa: Optional[str] = None
    titulo: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_email: Optional[str] = None
    contacto_telefono: Optional[str] = None
    descripcion: Optional[str] = None
    etapa: Optional[EtapaOportunidad] = None
    valor_estimado: Optional[float] = None
    probabilidad: Optional[int] = None
    orden: Optional[int] = None
    responsable: Optional[str] = None
    proxima_accion: Optional[str] = None
    fecha_cierre_estimada: Optional[date] = None
    proyecto_id: Optional[int] = None


class OportunidadOut(BaseModel):
    id: int
    empresa: str
    contacto_nombre: Optional[str]
    contacto_email: Optional[str]
    contacto_telefono: Optional[str]
    titulo: str
    descripcion: Optional[str]
    etapa: EtapaOportunidad = EtapaOportunidad.lead
    valor_estimado: float = 0.0
    probabilidad: int = 0
    orden: int = 0
    fuente: FuenteOportunidad = FuenteOportunidad.manual
    external_id: Optional[str]
    responsable: Optional[str]
    proxima_accion: Optional[str]
    fecha_cierre_estimada: Optional[date]
    proyecto_id: Optional[int]
    # ── Outreach del Equipo de Venta y Prospección ──
    idioma: Optional[str] = None
    disparador: Optional[str] = None
    mensaje_asunto: Optional[str] = None
    mensaje_cuerpo: Optional[str] = None
    outreach_status: Optional[str] = None
    respuesta_recibida: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class OportunidadExternal(BaseModel):
    """Payload del endpoint externo (API Key). `external_id` permite upsert
    idempotente: si ya existe una oportunidad con ese id, se actualiza."""
    external_id: str = Field(min_length=1)
    empresa: str = Field(min_length=1)
    titulo: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_email: Optional[str] = None
    contacto_telefono: Optional[str] = None
    descripcion: Optional[str] = None
    etapa: Optional[EtapaOportunidad] = None
    valor_estimado: Optional[float] = None
    probabilidad: Optional[int] = None
    responsable: Optional[str] = None
    proxima_accion: Optional[str] = None
    fecha_cierre_estimada: Optional[date] = None
    # ── Campos de outreach que carga el equipo ──
    idioma: Optional[str] = None
    disparador: Optional[str] = None
    mensaje_asunto: Optional[str] = None
    mensaje_cuerpo: Optional[str] = None
    outreach_status: Optional[str] = None
    respuesta_recibida: Optional[str] = None


# ── Contactos (base de prospección) ───────────────────────────────────────────

class ContactoCreate(BaseModel):
    empresa: str = Field(min_length=1)
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    info: Optional[str] = None
    origen: str = "manual"
    idioma: Optional[str] = None
    disparador: Optional[str] = None


class ContactoUpdate(BaseModel):
    empresa: Optional[str] = None
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    info: Optional[str] = None
    origen: Optional[str] = None
    estado: Optional[str] = None
    mensaje_asunto: Optional[str] = None
    mensaje_cuerpo: Optional[str] = None


class ContactoOut(BaseModel):
    id: int
    empresa: str
    nombre: Optional[str]
    email: Optional[str]
    telefono: Optional[str]
    info: Optional[str]
    origen: str = "agente"
    idioma: Optional[str]
    disparador: Optional[str]
    mensaje_asunto: Optional[str]
    mensaje_cuerpo: Optional[str]
    respuesta_recibida: Optional[str]
    estado: str = "nuevo"
    external_id: Optional[str]
    oportunidad_id: Optional[int]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ContactoExternal(BaseModel):
    """Payload del agente SDR (API Key). Upsert idempotente por external_id."""
    external_id: str = Field(min_length=1)
    empresa: str = Field(min_length=1)
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    info: Optional[str] = None
    origen: Optional[str] = None
    idioma: Optional[str] = None
    disparador: Optional[str] = None
    mensaje_asunto: Optional[str] = None
    mensaje_cuerpo: Optional[str] = None
    estado: Optional[str] = None        # nuevo/escrito/contactado


# ── Lead Jobs (cola de búsqueda) ──────────────────────────────────────────────

class LeadJobCreate(BaseModel):
    icp: dict
    cantidad: int = 20
    fundamento: Optional[str] = None


class LeadJobUpdate(BaseModel):
    status: Optional[str] = None
    resumen: Optional[str] = None


class LeadJobOut(BaseModel):
    id: int
    icp: dict
    cantidad: int
    status: str
    fundamento: Optional[str]
    resumen: Optional[str]
    created_at: Optional[datetime] = None
    processed_at: Optional[datetime]

    class Config:
        from_attributes = True


# ── Chat persistente equipo ↔ humano ──────────────────────────────────────────

class ChatMensajeCreate(BaseModel):
    contenido: str
    requiere_aprobacion: bool = False
    canal: str = "crm"


class ChatMensajeOut(BaseModel):
    id: int
    canal: str = "crm"
    rol: str
    contenido: str
    requiere_aprobacion: bool
    estado: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Centro de Agentes (orquestación) ──────────────────────────────────────────

# Roles válidos = los 3 equipos del documento Vibe Marketing (Marketing, Comercial, Desarrollo).
AGENTES_VALIDOS = {
    # Marketing
    "investigacion", "contenido", "creativo", "programador", "metricas", "ads",
    # Comercial
    "sdr", "calificacion", "agenda", "crm", "propuestas",
    # Desarrollo
    "relevador", "planificador", "desarrollador", "revisor", "qa", "devops", "soporte", "documentador",
}


class AgenteTareaCreate(BaseModel):
    agente: str = Field(min_length=1)
    instruccion: str = Field(min_length=1)
    contexto: dict = {}
    prioridad: str = "media"
    origen: str = "orquestador"


class AgenteTareaUpdate(BaseModel):
    estado: Optional[str] = None         # en_proceso/completado/error/requiere_aprobacion
    resultado: Optional[str] = None


class AgenteTareaOut(BaseModel):
    id: int
    agente: str
    instruccion: str
    contexto: dict = {}
    estado: str
    resultado: Optional[str] = None
    origen: str
    prioridad: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Aviso por mail (lo dispara el agente vía API key) ─────────────────────────

class FunnelNotify(BaseModel):
    asunto: str
    titulo: str
    subtitulo: Optional[str] = ""
    cuerpo: str                        # HTML simple o texto
    prioridad: Optional[str] = "info"  # info/alerta


class RespuestaInbound(BaseModel):
    """Respuesta entrante de un lead (la trae n8n desde el inbox). Matchea por email."""
    email: str
    texto: str
    asunto: Optional[str] = None


class CRMStats(BaseModel):
    total_oportunidades: int
    valor_pipeline: float          # suma de valor_estimado de oportunidades abiertas
    valor_ganado: float
    ganadas: int
    perdidas: int
    por_etapa: dict                # { etapa: {count, valor} }


# ── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardHUD(BaseModel):
    total_proyectos: int
    proyectos_activos: int
    total_tareas: int
    tareas_pendientes: int
    tareas_completadas: int
    total_requerimientos: int
    requerimientos_nuevos: int
    horas_semana: float


# ── Marketing · Meta Ads ──────────────────────────────────────────────────────

class AdMetricOut(BaseModel):
    fecha: date
    impresiones: int
    alcance: int
    clicks: int
    gasto: float
    ctr: float
    cpc: float
    cpm: float
    frecuencia: float
    conversiones: float
    valor_conversiones: float
    costo_conversion: float
    roas: float

    class Config:
        from_attributes = True


class AdCampaignOut(BaseModel):
    id: int
    external_id: str
    plataforma: str = "meta"
    nombre: str
    estado: str = "ACTIVE"
    objetivo: Optional[str] = None
    cuenta_id: Optional[str] = None
    cuenta_nombre: Optional[str] = None
    presupuesto_diario: Optional[float] = None
    moneda: str = "ARS"
    ultima_sync: Optional[datetime] = None
    # agregados del rango consultado (los calcula el endpoint)
    gasto_total: float = 0.0
    impresiones_total: int = 0
    clicks_total: int = 0
    conversiones_total: float = 0.0
    ctr_prom: float = 0.0
    cpc_prom: float = 0.0
    roas_prom: float = 0.0

    class Config:
        from_attributes = True


class AdRecommendationOut(BaseModel):
    id: int
    external_id: str
    campaign_id: Optional[int] = None
    tipo: str
    severidad: str
    titulo: str
    detalle: Optional[str] = None
    accion_sugerida: Optional[str] = None
    metricas_clave: dict = {}
    estado: str
    created_at: Optional[datetime] = None
    # nombre de la campaña (lo completa el endpoint para la UI)
    campana_nombre: Optional[str] = None

    class Config:
        from_attributes = True


class AdsOverview(BaseModel):
    conectado: bool
    ultima_sync: Optional[datetime] = None
    rango_dias: int
    campanas_total: int
    campanas_activas: int
    gasto_total: float
    impresiones_total: int
    clicks_total: int
    conversiones_total: float
    ctr_prom: float
    cpc_prom: float
    cpm_prom: float
    roas_prom: float
    recomendaciones_nuevas: int
    serie_gasto: List[dict] = []        # [{fecha, gasto, conversiones}]


# Entrada del agente analista (API key) — sincroniza campanas + métricas en lote.

class AdMetricIn(BaseModel):
    fecha: date
    impresiones: int = 0
    alcance: int = 0
    clicks: int = 0
    gasto: float = 0.0
    ctr: float = 0.0
    cpc: float = 0.0
    cpm: float = 0.0
    frecuencia: float = 0.0
    conversiones: float = 0.0
    valor_conversiones: float = 0.0
    costo_conversion: float = 0.0
    roas: float = 0.0


class AdCampaignIn(BaseModel):
    external_id: str = Field(min_length=1)
    nombre: str = Field(min_length=1)
    plataforma: str = "meta"
    estado: str = "ACTIVE"
    objetivo: Optional[str] = None
    cuenta_id: Optional[str] = None
    cuenta_nombre: Optional[str] = None
    presupuesto_diario: Optional[float] = None
    moneda: str = "ARS"
    metricas: List[AdMetricIn] = []


class AdSyncIn(BaseModel):
    """Payload del agente: lote de campanas con sus métricas diarias."""
    campanas: List[AdCampaignIn]


class AdRecommendationIn(BaseModel):
    external_id: str = Field(min_length=1)
    campaign_external_id: Optional[str] = None   # para vincular a la campaña
    tipo: str = "ajuste"
    severidad: str = "media"
    titulo: str = Field(min_length=1)
    detalle: Optional[str] = None
    accion_sugerida: Optional[str] = None
    metricas_clave: dict = {}


class AdRecommendationsIn(BaseModel):
    recomendaciones: List[AdRecommendationIn]


TokenResponse.model_rebuild()
