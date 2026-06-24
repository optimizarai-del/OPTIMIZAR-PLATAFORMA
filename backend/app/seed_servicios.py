"""Catálogo inicial de servicios de OPTIMIZAR. Idempotente: solo inserta si la
tabla está vacía. Basado en los candidatos a empaquetar del portfolio real."""
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

SERVICIOS_BASE = [
    {
        "nombre": "Agente conversacional WhatsApp/Telegram",
        "categoria": "Agentes",
        "descripcion": "Bot conversacional por rubro que atiende consultas, califica y deriva a un humano.",
        "capacidades": "WhatsApp Business API, Telegram, respuestas automáticas, calificación de leads, agendamiento, handoff a asesor, integración con CRM.",
        "base_referencia": "Tommy/Tomi (seguros, eventos, inmobiliaria)",
    },
    {
        "nombre": "Agente de voz para calificación y booking",
        "categoria": "Agentes",
        "descripcion": "Agente de voz que califica leads entrantes y agenda reuniones automáticamente.",
        "capacidades": "Llamadas de voz, calificación, agenda en calendario, derivación, integración con ventas.",
        "base_referencia": "Antonio de CaRBnB",
    },
    {
        "nombre": "Generación automática de contratos y documentos",
        "categoria": "Automatización",
        "descripcion": "Genera contratos y documentos a partir de datos, con plantillas por rubro.",
        "capacidades": "Google Docs, plantillas, llenado automático de datos, exportación a PDF, envío por mail.",
        "base_referencia": "SONNER + Ciudad Negocios",
    },
    {
        "nombre": "Sistema de reportes automatizados",
        "categoria": "Automatización",
        "descripcion": "Reportes recurrentes automáticos para estudios contables y administración.",
        "capacidades": "Extracción de datos, armado de reportes, KPIs, logging de conversaciones, envío programado por mail.",
        "base_referencia": "Riesco + Larrañaga",
    },
    {
        "nombre": "Plataforma de automatización contable AFIP/ARCA",
        "categoria": "Plataforma",
        "descripcion": "Automatización contable completa (AFIP/ARCA, IVA, banking, DGR, Onvio). Producto propio.",
        "capacidades": "Facturación electrónica AFIP, CAE, IVA, conciliación bancaria, DGR, Onvio, dashboard contable. Python + FastAPI + Supabase + React.",
        "base_referencia": "Larrañaga (IP 100% OPTIMIZAR)",
    },
    {
        "nombre": "Dashboard analítico / BI a medida",
        "categoria": "Dashboards",
        "descripcion": "Panel ejecutivo en tiempo real con KPIs conectado al ERP/sistema del cliente.",
        "capacidades": "ETL desde Tango/Holistor/ERP, KPIs de ventas/stock/cobranzas, gráficos, React + Recharts.",
        "base_referencia": "Distribuidora Norte / RetailMax",
    },
]


def seed_servicios_si_vacio(engine: Engine) -> None:
    from app.models import Servicio
    with Session(engine) as db:
        if db.query(Servicio).count() > 0:
            return
        db.add_all([Servicio(**s) for s in SERVICIOS_BASE])
        db.commit()
