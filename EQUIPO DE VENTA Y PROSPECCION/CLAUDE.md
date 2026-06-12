# EQUIPO DE VENTA Y PROSPECCIÓN

## Qué es este proyecto
Máquina de ventas autónoma hecha de subagentes de Claude Code. Un equipo digital que cada día
busca leads con criterio, escribe emails personalizados en el idioma del lead, los envía, escucha
las respuestas, y mejora con el tiempo. El humano solo da seguimiento a lo que responde.

## Restricción arquitectónica (NO negociable)
- Usar SIEMPRE el plan de Claude. NUNCA la API de Anthropic.
- El motor es un *scheduled cloud agent* (`/schedule`) facturado al plan.
- Patrón de polling invertido: la plataforma OPTIMIZAR encola/guarda config; Claude Code consume
  y devuelve resultados vía el endpoint externo `POST /api/crm/external/oportunidades`
  (API Key `X-API-Key`, upsert idempotente por `external_id`) que YA existe en `../OPTIMIZAR PF/app`.

## El equipo (.claude/agents/)
- `funnel-coo` — Director de Operaciones. Estratega diario: lee última corrida + CRM, decide qué buscar con fundamentos.
- `cold-lead-finder` — busca los mejores leads; trae idioma y contexto de cada uno.
- `sales-copywriter` — escribe el email + follow-ups en el idioma del lead.
- `funnel-orchestrator` — "el empleado": habla por el chat, gestiona aprobaciones, reporta, notifica.
- `agent-improver` — I+D: busca best practices y PROPONE mejoras a los agentes (solo aplica con aprobación + git).
- `inbox-responder` — clasifica las respuestas que llegan.
- `automation-developer` — diseña el envío/escucha (n8n).

## Estado y memoria del funnel (funnel/)
- `funnel/estado.md` — memoria continua entre corridas (qué se hizo, gotchas, estado de la tarea).
- `funnel/estrategia/<fecha>.md` — briefing diario del COO.
- `funnel/mejoras/<fecha>.md` — propuestas y mejoras aplicadas por el agent-improver.
- `funnel/leads/` — leads encontrados (`new/`) y cola de envío (`outbox/`).

## Notificaciones
Todo reporte y alerta se envía (vía `email_service.py` de la plataforma) a AMBOS correos:
- rodriguezfederico765@gmail.com
- optimizar.ai@gmail.com

## Estado de construcción (al 2026-06-12 — TODO deployado en producción)
- [x] Fase 1 — Equipo de agentes (idioma, estrategia, mejora continua).
- [x] Fase 2 — Backend: chat, lead_jobs, campos de outreach, migrador, notif a 2 mails.
- [x] Fase 3 — Scheduled cloud agent diario (`equipo-ventas-ciclo-diario`) en modo borrador.
- [x] Fase 4 — UI Prospección IA (chat + aprobaciones + búsqueda) en `frontend/src/pages/Prospeccion.jsx`.
- [x] Envío + escucha EN CÓDIGO (`outreach_service.py` + `scheduler.py`), apagado por defecto. (n8n queda como fallback.)
- [x] Chat en vivo: backend dispara la routine `chat-responder` (sobre el plan) al recibir un mensaje.
- [ ] PENDIENTE: validar calidad de emails → encender envío real (`OUTREACH_ENABLED=true` + warm-up).

## Cómo arrancar un ciclo manualmente (mientras no esté la Fase 3)
Invocar al `funnel-orchestrator`, que llama primero al `funnel-coo` (estrategia), luego al
`cold-lead-finder` y al `sales-copywriter`, y reporta. Las decisiones sensibles esperan tu aprobación.
