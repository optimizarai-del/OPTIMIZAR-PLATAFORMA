"""python -m app.seed"""
from datetime import date, datetime, timedelta
from app.database import SessionLocal, engine
from app.models import (Base, User, UserRole, Proyecto, ProyectoStatus,
                        PuntoAccion, Tarea, TareaStatus, TareaPrioridad,
                        RegistroTiempo, TipoRegistro, Requerimiento, RequerimientoStatus)
from app.security import hash_pw

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if db.query(User).count() > 0:
    print("Ya hay datos. Saliendo sin modificar la BD.")
    db.close()
    exit()

# ── Usuarios ──────────────────────────────────────────────────────────────────
admin   = User(nombre="Federico Rodríguez", email="admin@optimizar.com",
               password_hash=hash_pw("demo1234"), role=UserRole.admin)
manager = User(nombre="Martín Ruiz", email="martin@optimizar.com",
               password_hash=hash_pw("demo1234"), role=UserRole.manager)
dev1    = User(nombre="Lucía Torres", email="lucia@optimizar.com",
               password_hash=hash_pw("demo1234"), role=UserRole.developer)
dev2    = User(nombre="Tomás Benítez", email="tomas@optimizar.com",
               password_hash=hash_pw("demo1234"), role=UserRole.developer)
viewer  = User(nombre="Ana Comercial", email="ana@optimizar.com",
               password_hash=hash_pw("demo1234"), role=UserRole.viewer)
db.add_all([admin, manager, dev1, dev2, viewer])
db.commit()

# ── PROYECTO 1 — Facturación AFIP (en progreso, 60%) ─────────────────────────
p1 = Proyecto(
    nombre="Automatización Facturación AFIP",
    cliente="Estudio Contable López & Asociados",
    descripcion="Integración con AFIP para emisión automática de facturas electrónicas tipo A, B y C. Incluye CAE, PDF y envío automático por mail.",
    status=ProyectoStatus.en_progreso, color="#6366F1",
    fecha_inicio=date(2026, 3, 1), fecha_fin=date(2026, 6, 30),
    created_by=admin.id,
)
db.add(p1); db.commit()

puntos_p1 = [
    PuntoAccion(proyecto_id=p1.id, titulo="Relevamiento del proceso actual", orden=0, completado=True),
    PuntoAccion(proyecto_id=p1.id, titulo="Configuración de certificados AFIP (WSAA)", orden=1, completado=True),
    PuntoAccion(proyecto_id=p1.id, titulo="Desarrollo módulo de generación de CAE", orden=2, completado=True),
    PuntoAccion(proyecto_id=p1.id, titulo="Generación automática de PDF y envío por mail", orden=3, completado=False),
    PuntoAccion(proyecto_id=p1.id, titulo="Testing en ambiente de homologación AFIP", orden=4, completado=False),
    PuntoAccion(proyecto_id=p1.id, titulo="Deploy a producción y capacitación al cliente", orden=5, completado=False),
]
db.add_all(puntos_p1)

t1_1 = Tarea(proyecto_id=p1.id, titulo="Mapear endpoints WSFE y WSAA de AFIP",
             descripcion="Documentar todos los métodos SOAP necesarios para factura electrónica.",
             status=TareaStatus.completada, prioridad=TareaPrioridad.alta,
             asignado_a=dev1.id, fecha_inicio=date(2026, 3, 1),
             fecha_fin_estimada=date(2026, 3, 10), fecha_fin_real=date(2026, 3, 8),
             minutos_estimados=240)
t1_2 = Tarea(proyecto_id=p1.id, titulo="Implementar autenticación WSAA (token/sign)",
             descripcion="Generar y renovar tokens de acceso a los web services de AFIP.",
             status=TareaStatus.completada, prioridad=TareaPrioridad.urgente,
             asignado_a=dev1.id, fecha_inicio=date(2026, 3, 10),
             fecha_fin_estimada=date(2026, 3, 20), fecha_fin_real=date(2026, 3, 19),
             minutos_estimados=480)
t1_3 = Tarea(proyecto_id=p1.id, titulo="Módulo de solicitud de CAE (FECAESolicitar)",
             descripcion="Llamada al servicio WSFE para autorizar comprobantes y obtener CAE.",
             status=TareaStatus.completada, prioridad=TareaPrioridad.urgente,
             asignado_a=dev1.id, fecha_inicio=date(2026, 3, 20),
             fecha_fin_estimada=date(2026, 4, 5), fecha_fin_real=date(2026, 4, 3),
             minutos_estimados=720)
t1_4 = Tarea(proyecto_id=p1.id, titulo="Generación de PDF con datos del comprobante",
             descripcion="Template PDF con QR AFIP, datos del emisor, receptor, importes e IVA.",
             status=TareaStatus.en_progreso, prioridad=TareaPrioridad.alta,
             asignado_a=dev1.id, fecha_inicio=date(2026, 4, 5),
             fecha_fin_estimada=date(2026, 4, 20),
             minutos_estimados=360)
t1_5 = Tarea(proyecto_id=p1.id, titulo="Envío automático por mail con adjunto PDF",
             descripcion="Integración con SMTP / SendGrid para notificar al cliente al emitir.",
             status=TareaStatus.pendiente, prioridad=TareaPrioridad.media,
             asignado_a=dev2.id, fecha_inicio=date(2026, 4, 20),
             fecha_fin_estimada=date(2026, 5, 1),
             minutos_estimados=180)
t1_6 = Tarea(proyecto_id=p1.id, titulo="Testing end-to-end en homologación",
             descripcion="Pruebas con CAE de prueba y facturas de distinto tipo (A, B, C).",
             status=TareaStatus.pendiente, prioridad=TareaPrioridad.alta,
             asignado_a=dev1.id, fecha_inicio=date(2026, 5, 1),
             fecha_fin_estimada=date(2026, 5, 15),
             minutos_estimados=480)
db.add_all([t1_1, t1_2, t1_3, t1_4, t1_5, t1_6]); db.commit()

registros_p1 = [
    RegistroTiempo(tarea_id=t1_1.id, user_id=dev1.id, minutos=240,
                   descripcion="Lectura documentación AFIP y mapeo completo",
                   resultado="Lista de 12 endpoints relevados con parámetros",
                   tipo=TipoRegistro.manual, fecha=date(2026, 3, 8)),
    RegistroTiempo(tarea_id=t1_2.id, user_id=dev1.id, minutos=300,
                   descripcion="Implementación WSAA + generación de certificados",
                   resultado="Token y sign funcionando correctamente",
                   tipo=TipoRegistro.timer, fecha=date(2026, 3, 15)),
    RegistroTiempo(tarea_id=t1_2.id, user_id=dev1.id, minutos=180,
                   descripcion="Fix renovación automática de tokens expirados",
                   resultado="Auto-renovación cada 12 hs implementada",
                   tipo=TipoRegistro.timer, fecha=date(2026, 3, 18)),
    RegistroTiempo(tarea_id=t1_3.id, user_id=dev1.id, minutos=420,
                   descripcion="Desarrollo del módulo de solicitud de CAE",
                   resultado="Facturas tipo B funcionando en homologación",
                   tipo=TipoRegistro.timer, fecha=date(2026, 3, 28)),
    RegistroTiempo(tarea_id=t1_3.id, user_id=dev1.id, minutos=300,
                   descripcion="Soporte para facturas tipo A y C + notas de crédito",
                   resultado="Todos los tipos de comprobante implementados",
                   tipo=TipoRegistro.manual, fecha=date(2026, 4, 2)),
    RegistroTiempo(tarea_id=t1_4.id, user_id=dev1.id, minutos=180,
                   descripcion="Template base del PDF con datos fijos",
                   resultado="Estructura del PDF lista, falta QR",
                   tipo=TipoRegistro.timer, fecha=date(2026, 4, 8)),
    RegistroTiempo(tarea_id=t1_4.id, user_id=dev1.id, minutos=120,
                   descripcion="Integración del código QR AFIP en el PDF",
                   resultado="QR generado y validado en portal AFIP",
                   tipo=TipoRegistro.timer, fecha=date(2026, 4, 14)),
]
db.add_all(registros_p1)

# ── PROYECTO 2 — Bot WhatsApp (en progreso, 40%) ──────────────────────────────
p2 = Proyecto(
    nombre="Bot WhatsApp Atención al Cliente",
    cliente="Inmobiliaria Meridiano",
    descripcion="Bot conversacional en WhatsApp Business API para responder consultas de propiedades, agendar visitas y derivar a un asesor humano cuando sea necesario.",
    status=ProyectoStatus.en_progreso, color="#10B981",
    fecha_inicio=date(2026, 4, 1), fecha_fin=date(2026, 7, 15),
    created_by=admin.id,
)
db.add(p2); db.commit()

puntos_p2 = [
    PuntoAccion(proyecto_id=p2.id, titulo="Mapeo de flujos conversacionales", orden=0, completado=True),
    PuntoAccion(proyecto_id=p2.id, titulo="Alta de cuenta WhatsApp Business API (Meta)", orden=1, completado=True),
    PuntoAccion(proyecto_id=p2.id, titulo="Desarrollo de flujos con n8n", orden=2, completado=False),
    PuntoAccion(proyecto_id=p2.id, titulo="Integración con CRM de propiedades", orden=3, completado=False),
    PuntoAccion(proyecto_id=p2.id, titulo="Testing con usuarios reales y ajustes", orden=4, completado=False),
]
db.add_all(puntos_p2)

t2_1 = Tarea(proyecto_id=p2.id, titulo="Definir árbol de decisión del bot",
             descripcion="Mapear todos los casos de uso: consulta de precio, disponibilidad, agenda de visita, contacto asesor.",
             status=TareaStatus.completada, prioridad=TareaPrioridad.alta,
             asignado_a=manager.id, fecha_inicio=date(2026, 4, 1),
             fecha_fin_estimada=date(2026, 4, 7), fecha_fin_real=date(2026, 4, 6),
             minutos_estimados=240)
t2_2 = Tarea(proyecto_id=p2.id, titulo="Configurar webhook WhatsApp Business API",
             descripcion="Setup de cuenta Meta Business, verificación de webhook y tokens.",
             status=TareaStatus.completada, prioridad=TareaPrioridad.urgente,
             asignado_a=dev2.id, fecha_inicio=date(2026, 4, 7),
             fecha_fin_estimada=date(2026, 4, 14), fecha_fin_real=date(2026, 4, 13),
             minutos_estimados=300)
t2_3 = Tarea(proyecto_id=p2.id, titulo="Flujo de consulta de propiedades disponibles",
             descripcion="El bot consulta la API interna y devuelve las propiedades que matchean con los criterios del usuario.",
             status=TareaStatus.en_progreso, prioridad=TareaPrioridad.alta,
             asignado_a=dev2.id, fecha_inicio=date(2026, 4, 14),
             fecha_fin_estimada=date(2026, 4, 28),
             minutos_estimados=480)
t2_4 = Tarea(proyecto_id=p2.id, titulo="Flujo de agendamiento de visitas",
             descripcion="Integración con Google Calendar para verificar disponibilidad y agendar visita automáticamente.",
             status=TareaStatus.pendiente, prioridad=TareaPrioridad.media,
             asignado_a=dev2.id, fecha_inicio=date(2026, 4, 28),
             fecha_fin_estimada=date(2026, 5, 12),
             minutos_estimados=360)
t2_5 = Tarea(proyecto_id=p2.id, titulo="Handoff a asesor humano (escalamiento)",
             descripcion="Cuando el bot no puede resolver, notifica al asesor de turno por WhatsApp con el contexto de la conversación.",
             status=TareaStatus.pendiente, prioridad=TareaPrioridad.media,
             asignado_a=dev2.id, fecha_inicio=date(2026, 5, 12),
             fecha_fin_estimada=date(2026, 5, 20),
             minutos_estimados=180)
db.add_all([t2_1, t2_2, t2_3, t2_4, t2_5]); db.commit()

registros_p2 = [
    RegistroTiempo(tarea_id=t2_1.id, user_id=manager.id, minutos=180,
                   descripcion="Workshop con cliente para mapear casos de uso",
                   resultado="Árbol de 6 flujos principales definidos",
                   tipo=TipoRegistro.manual, fecha=date(2026, 4, 4)),
    RegistroTiempo(tarea_id=t2_2.id, user_id=dev2.id, minutos=240,
                   descripcion="Configuración Meta Business + webhook verificado",
                   resultado="Mensajes entrando correctamente al webhook",
                   tipo=TipoRegistro.timer, fecha=date(2026, 4, 11)),
    RegistroTiempo(tarea_id=t2_3.id, user_id=dev2.id, minutos=180,
                   descripcion="Primer flujo de consulta de propiedades funcionando",
                   resultado="Responde con lista de propiedades filtradas por zona",
                   tipo=TipoRegistro.timer, fecha=date(2026, 4, 18)),
    RegistroTiempo(tarea_id=t2_3.id, user_id=dev2.id, minutos=120,
                   descripcion="Mejora del formato de respuesta con imágenes",
                   resultado="Bot envía foto + descripción de cada propiedad",
                   tipo=TipoRegistro.timer, fecha=date(2026, 4, 22)),
]
db.add_all(registros_p2)

# ── PROYECTO 3 — Dashboard Analítico (planificacion) ──────────────────────────
p3 = Proyecto(
    nombre="Dashboard Analítico de Ventas",
    cliente="Distribuidora Norte S.R.L.",
    descripcion="Panel ejecutivo en tiempo real con KPIs de ventas, stock, cobranzas y rentabilidad por producto, zona y vendedor. Conectado a Tango.",
    status=ProyectoStatus.planificacion, color="#F59E0B",
    fecha_inicio=date(2026, 5, 15), fecha_fin=date(2026, 8, 31),
    created_by=manager.id,
)
db.add(p3); db.commit()

puntos_p3 = [
    PuntoAccion(proyecto_id=p3.id, titulo="Relevamiento de KPIs prioritarios", orden=0, completado=False),
    PuntoAccion(proyecto_id=p3.id, titulo="Conexión y extracción de datos desde Tango", orden=1, completado=False),
    PuntoAccion(proyecto_id=p3.id, titulo="Modelo de datos y ETL", orden=2, completado=False),
    PuntoAccion(proyecto_id=p3.id, titulo="Desarrollo del dashboard (React + Recharts)", orden=3, completado=False),
    PuntoAccion(proyecto_id=p3.id, titulo="Capacitación y entrega", orden=4, completado=False),
]
db.add_all(puntos_p3)

t3_1 = Tarea(proyecto_id=p3.id, titulo="Relevamiento de KPIs con gerencia",
             descripcion="Reunión para definir qué métricas son prioritarias para el panel ejecutivo.",
             status=TareaStatus.pendiente, prioridad=TareaPrioridad.alta,
             asignado_a=manager.id, fecha_inicio=date(2026, 5, 15),
             fecha_fin_estimada=date(2026, 5, 22),
             minutos_estimados=180)
t3_2 = Tarea(proyecto_id=p3.id, titulo="Analizar estructura de BD de Tango",
             descripcion="Identificar tablas de ventas, stock y cobranzas en la base de Tango.",
             status=TareaStatus.pendiente, prioridad=TareaPrioridad.alta,
             asignado_a=dev1.id, fecha_inicio=date(2026, 5, 22),
             fecha_fin_estimada=date(2026, 6, 5),
             minutos_estimados=240)
t3_3 = Tarea(proyecto_id=p3.id, titulo="Diseño del modelo de datos del dashboard",
             descripcion="Definir esquema de tablas desnormalizadas para consultas rápidas.",
             status=TareaStatus.pendiente, prioridad=TareaPrioridad.media,
             asignado_a=dev1.id, fecha_inicio=date(2026, 6, 5),
             fecha_fin_estimada=date(2026, 6, 20),
             minutos_estimados=300)
db.add_all([t3_1, t3_2, t3_3]); db.commit()

# ── PROYECTO 4 — ERP + E-commerce (completado) ───────────────────────────────
p4 = Proyecto(
    nombre="Integración ERP + Tienda Online",
    cliente="RetailMax S.A.",
    descripcion="Sincronización bidireccional entre Holistor y WooCommerce. Stock, precios y órdenes actualizados en tiempo real sin intervención manual.",
    status=ProyectoStatus.completado, color="#8B5CF6",
    fecha_inicio=date(2026, 1, 10), fecha_fin=date(2026, 3, 28),
    created_by=admin.id,
)
db.add(p4); db.commit()

puntos_p4 = [
    PuntoAccion(proyecto_id=p4.id, titulo="Análisis de APIs de Holistor y WooCommerce", orden=0, completado=True),
    PuntoAccion(proyecto_id=p4.id, titulo="Middleware de sincronización (n8n)", orden=1, completado=True),
    PuntoAccion(proyecto_id=p4.id, titulo="Sincronización de stock en tiempo real", orden=2, completado=True),
    PuntoAccion(proyecto_id=p4.id, titulo="Sincronización de precios y listas", orden=3, completado=True),
    PuntoAccion(proyecto_id=p4.id, titulo="Ingreso automático de órdenes al ERP", orden=4, completado=True),
    PuntoAccion(proyecto_id=p4.id, titulo="Testing, go-live y documentación", orden=5, completado=True),
]
db.add_all(puntos_p4)

t4_1 = Tarea(proyecto_id=p4.id, titulo="Documentar endpoints API Holistor",
             status=TareaStatus.completada, prioridad=TareaPrioridad.alta,
             asignado_a=dev2.id, fecha_inicio=date(2026, 1, 10),
             fecha_fin_estimada=date(2026, 1, 20), fecha_fin_real=date(2026, 1, 18),
             minutos_estimados=300)
t4_2 = Tarea(proyecto_id=p4.id, titulo="Middleware de sincronización de stock",
             status=TareaStatus.completada, prioridad=TareaPrioridad.urgente,
             asignado_a=dev2.id, fecha_inicio=date(2026, 1, 20),
             fecha_fin_estimada=date(2026, 2, 10), fecha_fin_real=date(2026, 2, 8),
             minutos_estimados=600)
t4_3 = Tarea(proyecto_id=p4.id, titulo="Sincronización de precios por lista",
             status=TareaStatus.completada, prioridad=TareaPrioridad.alta,
             asignado_a=dev2.id, fecha_inicio=date(2026, 2, 10),
             fecha_fin_estimada=date(2026, 2, 25), fecha_fin_real=date(2026, 2, 22),
             minutos_estimados=360)
t4_4 = Tarea(proyecto_id=p4.id, titulo="Ingreso automático de órdenes WooCommerce → Holistor",
             status=TareaStatus.completada, prioridad=TareaPrioridad.urgente,
             asignado_a=dev1.id, fecha_inicio=date(2026, 2, 22),
             fecha_fin_estimada=date(2026, 3, 10), fecha_fin_real=date(2026, 3, 9),
             minutos_estimados=480)
t4_5 = Tarea(proyecto_id=p4.id, titulo="Testing, ajustes y documentación final",
             status=TareaStatus.completada, prioridad=TareaPrioridad.media,
             asignado_a=dev2.id, fecha_inicio=date(2026, 3, 10),
             fecha_fin_estimada=date(2026, 3, 28), fecha_fin_real=date(2026, 3, 26),
             minutos_estimados=240)
db.add_all([t4_1, t4_2, t4_3, t4_4, t4_5]); db.commit()

registros_p4 = [
    RegistroTiempo(tarea_id=t4_2.id, user_id=dev2.id, minutos=360,
                   descripcion="Desarrollo del webhook de stock con queue de reintentos",
                   resultado="Latencia < 30 seg entre cambio en Holistor y WooCommerce",
                   tipo=TipoRegistro.timer, fecha=date(2026, 2, 3)),
    RegistroTiempo(tarea_id=t4_4.id, user_id=dev1.id, minutos=300,
                   descripcion="Parsing de órdenes WooCommerce al formato Holistor",
                   resultado="Pedidos ingresando automáticamente con cliente y artículos",
                   tipo=TipoRegistro.timer, fecha=date(2026, 3, 5)),
]
db.add_all(registros_p4)

# ── Requerimientos ────────────────────────────────────────────────────────────
req1 = Requerimiento(
    nombre_cliente="Estudio López & Asociados",
    sector="Contabilidad / Impuestos",
    personas_reunion="Dr. Hernán López (socio), Lic. Ramírez (administración)",
    sistemas_core="Holistor, facturas manuales en Word",
    herramientas=["Excel / Google Sheets", "WhatsApp / Telegram", "Correo Electrónico (Gmail / Outlook)"],
    uso_ia="ChatGPT Plus ocasionalmente para redactar correos",
    tipos_acceso=["Entran con usuario y contraseña genéricos/compartidos."],
    estado_bd="Información en Excels separados por mes, sin servidor central",
    nombre_proceso="Emisión de facturas electrónicas AFIP",
    trigger_proceso="El cliente confirma el pago de honorarios por transferencia",
    pasos_manuales="1. Abrir portal AFIP. 2. Ingresar datos del cliente manualmente. 3. Completar importe y concepto. 4. Descargar PDF. 5. Enviar por mail.",
    volumen_proceso="~120 facturas/mes",
    tiempo_por_proceso="15-20 minutos por factura",
    responsable_comercial="Martín Ruiz",
    fecha_entrega=date(2026, 2, 28),
    status=RequerimientoStatus.convertido,
    proyecto_id=p1.id,
)
req2 = Requerimiento(
    nombre_cliente="Inmobiliaria Meridiano",
    sector="Inmobiliaria / Real Estate",
    personas_reunion="Ing. Carla Vega (gerente comercial), Juan Pérez (admin)",
    sistemas_core="CRM propio (interno), portal web WordPress",
    herramientas=["WhatsApp / Telegram", "Correo Electrónico (Gmail / Outlook)", "Excel / Google Sheets"],
    uso_ia="Sin uso de IA actualmente",
    tipos_acceso=["Tienen API propia documentada.", "Entran con usuario y contraseña genéricos/compartidos."],
    estado_bd="Base centralizada en servidor propio con acceso SQL",
    nombre_proceso="Atención de consultas de clientes por WhatsApp",
    trigger_proceso="Un potencial comprador envía mensaje al número de WhatsApp de la inmobiliaria",
    pasos_manuales="1. Empleado lee el mensaje. 2. Busca propiedades en el sistema. 3. Copia datos y envía manualmente. 4. Agenda visita en Google Calendar.",
    volumen_proceso="~200 consultas/mes",
    tiempo_por_proceso="8-12 minutos por consulta",
    responsable_comercial="Federico Rodríguez",
    fecha_entrega=date(2026, 3, 15),
    status=RequerimientoStatus.convertido,
    proyecto_id=p2.id,
)
req3 = Requerimiento(
    nombre_cliente="Distribuidora Norte S.R.L.",
    sector="Distribución / Logística",
    personas_reunion="Lic. Marcos Soria (gerente general), Cra. Funes (finanzas)",
    sistemas_core="Tango Gestión, planillas Excel de seguimiento",
    herramientas=["Excel / Google Sheets", "Correo Electrónico (Gmail / Outlook)", "Trello / Asana / ClickUp"],
    uso_ia="Sin uso de IA",
    tipos_acceso=["No saben / A confirmar por Desarrollo."],
    estado_bd="Tango como sistema central, reportes exportados a Excel manualmente",
    nombre_proceso="Reporte semanal de KPIs para gerencia",
    trigger_proceso="Cada lunes a las 9am el gerente necesita el reporte de la semana anterior",
    pasos_manuales="1. Exportar ventas de Tango. 2. Exportar stock. 3. Armar Excel con fórmulas. 4. Generar gráficos. 5. Enviar por mail a la gerencia.",
    volumen_proceso="1 reporte/semana (4 al mes)",
    tiempo_por_proceso="3-4 horas por reporte",
    responsable_comercial="Martín Ruiz",
    fecha_entrega=date(2026, 4, 20),
    status=RequerimientoStatus.aprobado,
    proyecto_id=p3.id,
)
req4 = Requerimiento(
    nombre_cliente="Clínica Médica San Martín",
    sector="Salud",
    personas_reunion="Dr. Navarro (director médico), Sra. Romero (administración)",
    sistemas_core="Sistema propio de turnos (web), Excel para facturación obras sociales",
    herramientas=["WhatsApp / Telegram", "Correo Electrónico (Gmail / Outlook)", "Excel / Google Sheets"],
    uso_ia="Sin uso de IA",
    tipos_acceso=["Cada empleado entra con sus credenciales personales (Ej. Clave Fiscal individual)."],
    estado_bd="Turnos en sistema web, facturación en Excels separados por obra social",
    nombre_proceso="Confirmación de turnos y recordatorios a pacientes",
    trigger_proceso="48 horas antes del turno del paciente",
    pasos_manuales="1. Exportar lista de turnos del día siguiente. 2. Enviar WhatsApp manualmente a cada paciente. 3. Registrar en Excel si confirmó o canceló.",
    volumen_proceso="~180 turnos/semana",
    tiempo_por_proceso="2-3 minutos por paciente",
    responsable_comercial="Federico Rodríguez",
    fecha_entrega=date(2026, 5, 5),
    status=RequerimientoStatus.nuevo,
)
req5 = Requerimiento(
    nombre_cliente="Ferretería El Torno",
    sector="Retail / Ferretería",
    personas_reunion="Sr. Gustavo Peña (dueño)",
    sistemas_core="Ninguno formal, todo en Excel",
    herramientas=["Excel / Google Sheets", "WhatsApp / Telegram"],
    uso_ia="ChatGPT gratuito para consultas puntuales",
    tipos_acceso=["No saben / A confirmar por Desarrollo."],
    estado_bd="Todo en Excels locales, sin backup automático",
    nombre_proceso="Control de stock y reposición de mercadería",
    trigger_proceso="Cuando un producto llega a menos de 5 unidades",
    pasos_manuales="El dueño revisa manualmente el Excel de stock cada día y llama al proveedor.",
    volumen_proceso="~30 productos reponer/semana",
    tiempo_por_proceso="45 minutos diarios de control",
    responsable_comercial="Martín Ruiz",
    fecha_entrega=date(2026, 5, 10),
    status=RequerimientoStatus.evaluacion,
)
db.add_all([req1, req2, req3, req4, req5])
db.commit()
db.close()

print("")
print("OK Seed completado con datos demo completos.")
print("")
print("  USUARIOS:")
print("  -----------------------------------------")
print("  admin@optimizar.com    / demo1234  (admin)")
print("  martin@optimizar.com   / demo1234  (manager)")
print("  lucia@optimizar.com    / demo1234  (developer)")
print("  tomas@optimizar.com    / demo1234  (developer)")
print("  ana@optimizar.com      / demo1234  (viewer)")
print("")
print("  PROYECTOS: 4 | TAREAS: 19 | REQUERIMIENTOS: 5")
print("")
