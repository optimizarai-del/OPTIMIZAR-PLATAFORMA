# OPTIMIZAR-OS — Cerebro de marca y orquestación

> Este repo es la capa **V (Visión) + I (Insumos)** del framework VIVE.
> No reemplaza a los agentes que ya corren en la plataforma — los **alimenta**.
> Regla de oro: *si la Visión es débil, los agentes solo amplifican mediocridad a escala.*

## Qué es esto

El "manual de la empresa" que todos los agentes de IA de OPTIMIZAR leen como
contexto permanente antes de generar nada (copy, creativos, emails, prospección).
Se escribe **una vez** y se usa **cientos de veces**.

## El framework VIVE

| Capa | Qué es | Dónde vive |
|------|--------|-----------|
| **V** Visión | ICP, oferta, ángulo, estrategia | `vibe/vision.md`, `vibe/icp.md`, `vibe/oferta.md` |
| **I** Insumos | Brand voice, casos, tono | `vibe/brand.md`, `vibe/casos.md`, `vibe/tono.md` |
| **V** Brain | Claude Code + subagentes + MCPs | `.claude/agents/` (acá) + agentes en la plataforma |
| **E** Engine | n8n + scheduled cloud agents | `engine/` (punteros) + OPTIMIZAR-PLATAFORMA |

## Cómo se usa (para cualquier agente)

**ANTES de generar cualquier output, todo agente DEBE leer:**
1. `vibe/brand.md` — quiénes somos y qué NO hacer
2. `vibe/icp.md` — a quién le hablamos
3. `vibe/tono.md` — cómo hablamos
4. El archivo específico de su tarea (`oferta.md` para vender, `casos.md` para prueba social)

Si un dato del `vibe/` dice `[POR DEFINIR]`, el agente **no inventa**: marca el hueco
y lo reporta, no lo rellena con suposiciones.

## Agentes en este repo (lado orgánico — lo que faltaba)

| Agente | Rol | Estado |
|--------|-----|--------|
| `investigacion` | Monitorea tendencias IA/competidores → reporte semanal de ideas | nuevo |
| `content-creator` | Genera posts/carruseles/reels para IG + LinkedIn | nuevo |
| `creative-designer` | Briefs de imágenes/gráficos on-brand | nuevo |
| `meta-ads-analyst` | Analiza Meta Ads (MCP Pipeboard) → recomendaciones a la plataforma | copiado de la plataforma |

> El MCP `meta-ads` se configura en `.mcp.json` (token en `.env`, ignorado por git).
> Se activa al abrir Claude Code dentro de este repo.

## Agentes que NO viven acá (ya corren en la plataforma)

No duplicar. Estos están en `OPTIMIZAR PF/app/`:
- **Ventas (7):** funnel-orchestrator, funnel-coo, cold-lead-finder, sales-copywriter,
  inbox-responder, automation-developer, agent-improver.
- **Marketing (1):** meta-ads-analyst (Meta Ads vía Pipeboard MCP).

Punto de integración: el scheduled cloud agent del funnel debe leer `vibe/` al arrancar.

## Restricción técnica (heredada del funnel)

- Motor = **scheduled cloud agent sobre el plan de Claude**, NUNCA la API de Anthropic.
- Polling invertido: la plataforma encola; Claude consume y devuelve por endpoint
  (`POST /api/crm/external/...`, `X-API-Key`, upsert idempotente).

## Estado del sistema

Ver `vibe/estado.md` para qué está definido y qué falta. El gran desbloqueante hoy
es **llenar los `[POR DEFINIR]`** en la reunión de equipo (ver `REUNION.md`).
