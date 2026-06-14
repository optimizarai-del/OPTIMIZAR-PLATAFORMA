# EQUIPO DE MARKETING — OPTIMIZAR

## Qué es
Área de marketing de OPTIMIZAR, hecha con agentes de Claude Code. Arranca con **performance**
(análisis de Meta Ads) y va a crecer hacia un **equipo de marketing creativo** (copy, creativos,
contenido). Todo corre sobre el plan de Claude — sin API de Anthropic — y se integra a la
plataforma OPTIMIZAR vía sus endpoints externos.

## Restricción arquitectónica (igual que el equipo de ventas)
- SIEMPRE el plan de Claude, NUNCA la API de Anthropic para el trabajo pesado.
- Patrón de polling invertido: el agente analiza sobre el plan y **empuja** resultados a la
  plataforma vía endpoints externos con `X-API-Key` (`/api/ads/external/*`).

## El equipo (.claude/agents/)
- `meta-ads-analyst` — **analista de performance**: se conecta por MCP a Meta Ads, baja campañas
  e insights, analiza tendencias, genera recomendaciones accionables y sincroniza todo a la plataforma.
- _(próximamente)_ equipo creativo: copywriter de ads, generador de conceptos creativos, calendarista de contenido.

## Conexión MCP — Meta Ads (Pipeboard)
El servidor MCP está en `.mcp.json` (`meta-ads` vía `uvx meta-ads-mcp`). Autenticación por Pipeboard:
1. Creá una cuenta en https://pipeboard.co y conectá tu cuenta de Meta (Facebook Business).
2. Generá un **API token** de Pipeboard.
3. Exportá la variable antes de abrir Claude Code en esta carpeta:
   - PowerShell: `$env:PIPEBOARD_API_TOKEN = "tu_token"`
   - bash: `export PIPEBOARD_API_TOKEN="tu_token"`
4. Necesitás `uv`/`uvx` instalado (https://docs.astral.sh/uv/). El servidor se baja solo con `uvx`.

> Alternativa sin Pipeboard: el servidor `meta-ads-mcp` también acepta un access token directo de
> la Graph API de Meta. Si preferís esa vía, cambiá el `.mcp.json` a `"env": {"META_ACCESS_TOKEN": "..."}`.

## Variables del backend que usa el agente
Al invocar al analista, pasale (o tenelas en el entorno):
- `SELF_API_BASE` / `API_BASE` — URL pública del backend OPTIMIZAR.
- `EXTERNAL_API_KEY` / `API_KEY` — clave del endpoint externo (la misma del CRM).

## Cómo correrlo
Abrí Claude Code en esta carpeta (con `PIPEBOARD_API_TOKEN` exportado) e invocá al
`meta-ads-analyst`: "analizá mis campañas de Meta y sincronizá con la plataforma". El agente:
1. baja campañas + insights de los últimos 14 días,
2. los empuja a `/api/ads/external/sync`,
3. analiza y deja recomendaciones en `/api/ads/external/recommendations`,
4. te reporta las acciones más importantes.

Las métricas y recomendaciones aparecen en la plataforma en **Marketing · Meta Ads**.

## Dónde se ve en la plataforma
- Frontend: `frontend/src/pages/Marketing.jsx` (ruta `/marketing`, solo manager).
- Backend: `backend/app/routers/ads.py` + modelos `AdCampaign` / `AdMetric` / `AdRecommendation`.
