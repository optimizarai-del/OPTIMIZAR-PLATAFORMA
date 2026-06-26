# engine/ — Capa E (motor autónomo)

Este repo NO duplica el motor. Acá solo viven los **punteros** a lo que ya corre.

## Lo que ya existe (OPTIMIZAR-PLATAFORMA)
- **Scheduled cloud agent** `equipo-ventas-ciclo-diario` — corre 12:00 UTC (9:00 ART),
  sobre el plan de Claude (NO API). Hoy en modo borrador / o push-vivo según config.
- **n8n self-hosted** (`n8n.optimizar-ia.com`) — pegamento de automatizaciones.
- **Endpoints de la plataforma:** `POST /api/crm/external/oportunidades`,
  `/api/ads/external/sync`, `X-API-Key`, upsert idempotente.

## Lo que falta enganchar (TODO)
1. Que el scheduled agent **lea `vibe/` al arrancar** (cargar brand/icp/tono como contexto).
2. Routine semanal que dispare al agente `investigacion` → reporte a `outputs/`.
3. Pipeline orgánico: investigacion → content-creator → creative-designer → aprobación humana → publicación.

## Restricción
Todo el motor corre **sobre el plan de Claude vía scheduled cloud agents**, nunca la API.
Polling invertido: la plataforma encola, Claude consume y devuelve por endpoint.
