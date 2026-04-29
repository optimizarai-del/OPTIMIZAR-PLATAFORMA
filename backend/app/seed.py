"""python -m app.seed"""
from datetime import date, datetime
from app.database import SessionLocal, engine
from app.models import Base, User, UserRole, Proyecto, ProyectoStatus, PuntoAccion, Tarea, TareaStatus, TareaPrioridad, RegistroTiempo, TipoRegistro, Requerimiento
from app.security import hash_pw

Base.metadata.create_all(bind=engine)

db = SessionLocal()

if db.query(User).count() > 0:
    print("Ya hay datos. Saliendo.")
    db.close()
    exit()

# Users
admin = User(nombre="Admin Optimizar", email="admin@optimizar.com",
             password_hash=hash_pw("demo1234"), role=UserRole.admin)
dev1 = User(nombre="Lucía Torres", email="lucia@optimizar.com",
            password_hash=hash_pw("demo1234"), role=UserRole.developer)
manager = User(nombre="Martín Ruiz", email="martin@optimizar.com",
               password_hash=hash_pw("demo1234"), role=UserRole.manager)
db.add_all([admin, dev1, manager])
db.commit()

# Proyecto 1
p1 = Proyecto(nombre="Automatización Facturación AFIP",
              cliente="Estudio Contable López",
              descripcion="Integración con AFIP para emisión automática de facturas electrónicas.",
              status=ProyectoStatus.en_progreso, color="#6366F1",
              fecha_inicio=date(2026, 3, 1), fecha_fin=date(2026, 6, 30),
              created_by=admin.id)
db.add(p1)
db.commit()

# Plan de acción P1
puntos_p1 = [
    PuntoAccion(proyecto_id=p1.id, titulo="Relevamiento de sistemas actuales", orden=0, completado=True),
    PuntoAccion(proyecto_id=p1.id, titulo="Configuración certificados AFIP", orden=1, completado=True),
    PuntoAccion(proyecto_id=p1.id, titulo="Desarrollo API de integración", orden=2, completado=False),
    PuntoAccion(proyecto_id=p1.id, titulo="Testing en ambiente homologación", orden=3, completado=False),
    PuntoAccion(proyecto_id=p1.id, titulo="Deploy a producción y capacitación", orden=4, completado=False),
]
db.add_all(puntos_p1)

# Tareas P1
t1 = Tarea(proyecto_id=p1.id, titulo="Mapear endpoints AFIP necesarios",
           status=TareaStatus.completada, prioridad=TareaPrioridad.alta,
           asignado_a=dev1.id, fecha_inicio=date(2026, 3, 1),
           fecha_fin_estimada=date(2026, 3, 10), fecha_fin_real=date(2026, 3, 9),
           minutos_estimados=240)
t2 = Tarea(proyecto_id=p1.id, titulo="Implementar módulo de generación de CAE",
           status=TareaStatus.en_progreso, prioridad=TareaPrioridad.urgente,
           asignado_a=dev1.id, fecha_inicio=date(2026, 3, 10),
           fecha_fin_estimada=date(2026, 4, 15), minutos_estimados=960)
t3 = Tarea(proyecto_id=p1.id, titulo="UI de carga manual de facturas",
           status=TareaStatus.pendiente, prioridad=TareaPrioridad.media,
           asignado_a=dev1.id, fecha_inicio=date(2026, 4, 1),
           fecha_fin_estimada=date(2026, 4, 30), minutos_estimados=480)
db.add_all([t1, t2, t3])
db.commit()

# Registros tiempo
r1 = RegistroTiempo(tarea_id=t1.id, user_id=dev1.id, minutos=240,
                    descripcion="Documentación y mapeo completo", resultado="Lista de endpoints definida",
                    tipo=TipoRegistro.manual, fecha=date(2026, 3, 9))
r2 = RegistroTiempo(tarea_id=t2.id, user_id=dev1.id, minutos=180,
                    descripcion="Sesión de desarrollo día 1", resultado="Estructura base del módulo",
                    tipo=TipoRegistro.timer, fecha=date(2026, 3, 11))
r3 = RegistroTiempo(tarea_id=t2.id, user_id=dev1.id, minutos=120,
                    descripcion="Continuación integración", resultado="Auth con WSAA funcionando",
                    tipo=TipoRegistro.timer, fecha=date(2026, 3, 12))
db.add_all([r1, r2, r3])

# Proyecto 2
p2 = Proyecto(nombre="Bot WhatsApp Atención Clientes",
              cliente="Inmobiliaria Meridiano",
              descripcion="Automatización de consultas frecuentes vía WhatsApp Business API.",
              status=ProyectoStatus.planificacion, color="#10B981",
              fecha_inicio=date(2026, 5, 1), fecha_fin=date(2026, 7, 31),
              created_by=admin.id)
db.add(p2)
db.commit()

puntos_p2 = [
    PuntoAccion(proyecto_id=p2.id, titulo="Definición de flujos conversacionales", orden=0, completado=False),
    PuntoAccion(proyecto_id=p2.id, titulo="Setup cuenta WhatsApp Business API", orden=1, completado=False),
    PuntoAccion(proyecto_id=p2.id, titulo="Desarrollo del bot con n8n", orden=2, completado=False),
]
db.add_all(puntos_p2)

# Requerimiento demo
req = Requerimiento(
    nombre_cliente="Estudio López & Asociados",
    sector="Contabilidad / Impuestos",
    personas_reunion="Dr. López (socio), Lic. Ramírez (administración)",
    sistemas_core="Holistor, facturas manuales en Word",
    herramientas=["Excel / Google Sheets", "WhatsApp / Telegram", "Correo Electrónico (Gmail / Outlook)"],
    uso_ia="ChatGPT Plus ocasionalmente",
    tipos_acceso=["Entran con usuario y contraseña genéricos/compartidos."],
    estado_bd="Información en Excels separados por mes",
    nombre_proceso="Emisión de facturas electrónicas AFIP",
    trigger_proceso="El estudio recibe confirmación de pago de honorarios del cliente",
    pasos_manuales="1. Abrir portal AFIP. 2. Ingresar datos del cliente manualmente. 3. Completar importe y concepto. 4. Descargar PDF. 5. Enviar por mail.",
    volumen_proceso="~120 facturas/mes",
    tiempo_por_proceso="15-20 minutos por factura",
    responsable_comercial="Martín Ruiz",
    fecha_entrega=date(2026, 4, 29),
    status="convertido",
    proyecto_id=p1.id,
)
db.add(req)
db.commit()
db.close()
print("✓ Seed completado.")
print("  admin@optimizar.com / demo1234")
print("  lucia@optimizar.com / demo1234")
print("  martin@optimizar.com / demo1234")
