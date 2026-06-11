# RUNBOOK — Ciclo del Equipo de Venta y Prospección (v1)

Contrato de integración entre el equipo de agentes (Claude Code) y la plataforma OPTIMIZAR.
Patrón de polling invertido: la plataforma encola/almacena; el equipo consume y devuelve.
**Sin API de Anthropic** — el equipo corre bajo el plan de Claude.

## Configuración (variables de entorno del backend)
En `backend/.env`:
```
EXTERNAL_API_KEY=<clave fuerte>           # protege los endpoints /external/* y /lead-jobs
FUNNEL_NOTIFY_EMAILS=rodriguezfederico765@gmail.com,optimizar.ai@gmail.com
NOTIFICATIONS_ENABLED=true                # + SMTP_HOST/USER/PASSWORD para que salgan los mails
```
Base URL de la API: `${API_BASE_URL}` (ej. https://<tu-dominio>/  ó http://localhost:8000)

## Endpoints que usa el equipo (todos con header `X-API-Key: $EXTERNAL_API_KEY`)
| Acción | Método | Ruta |
|---|---|---|
| Leer pedidos de búsqueda pendientes | GET | `/api/crm/lead-jobs/pending` |
| Marcar un job procesando/completado | PATCH | `/api/crm/lead-jobs/{id}` `{status, resumen}` |
| Cargar/actualizar un lead (idempotente) | POST | `/api/crm/external/oportunidades` |
| Postear mensaje del agente al chat | POST | `/api/crm/external/chat` `{contenido, requiere_aprobacion}` |
| Avisar por mail a los 2 correos | POST | `/api/crm/external/notify` `{asunto,titulo,subtitulo,cuerpo,prioridad}` |

El humano usa (con JWT, desde la plataforma): crear lead-jobs, leer/postear en el chat, aprobar/rechazar.

## El ciclo diario (lo ejecuta `funnel-orchestrator`)
1. **Estrategia** — invocar `funnel-coo`: lee `funnel/estado.md` + el CRM (`GET /api/crm/stats`) y
   decide el segmento. Si marca `Requiere aprobación: sí` → postear la pregunta en el chat
   (`/external/chat` con `requiere_aprobacion:true`), notificar por mail, y **esperar** la aprobación
   del humano (releer `/api/crm/chat` en la próxima corrida del `/loop`).
2. **Búsqueda** — invocar `cold-lead-finder` con el segmento aprobado. Trae leads con idioma + contexto.
3. **Escritura** — invocar `sales-copywriter` por lead (email en el idioma del lead).
4. **Carga al CRM** — por cada lead: `POST /external/oportunidades` con
   `external_id` (= lead_id), `empresa`, `contacto_*`, `idioma`, `disparador`,
   `mensaje_asunto`, `mensaje_cuerpo`, `outreach_status:"escrito"`, `etapa:"lead"`.
5. **Reporte** — `POST /external/notify` con el resumen (qué se buscó y por qué, cuántos leads,
   mejoras investigadas, errores/riesgos) y postearlo también en el chat. Marcar el job `completado`.
6. **Mejora (semanal)** — invocar `agent-improver`: propone cambios → al chat con `requiere_aprobacion`
   → aplicar solo tras OK + commit en git.

## Ejecución
- **Manual / semi-auto**: abrir Claude Code en esta carpeta y pedir "corré el ciclo de prospección".
  Para que sea constante, usar `/loop` (cada N minutos chequea jobs pendientes y aprobaciones).
- **Autónomo (futuro, Fase 3)**: un *scheduled cloud agent* (`/schedule`) corre el ciclo a diario,
  facturado al plan, con la PC apagada.

## Pendiente (no incluido en v1)
- Fase 4: página de chat + vista de seguimiento en `frontend/src/pages/CRM.jsx`.
- Fase 5: envío real de mails y escucha de respuestas (n8n + proveedor).
- Migración de columnas para la BD de producción (las columnas nuevas son nullable; en una BD
  existente hay que agregarlas con un ALTER, ya que `create_all` no altera tablas existentes).
