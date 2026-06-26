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

## Estructura: 3 Directores IA + sus equipos (doc Vibe Marketing FINAL)

El equipo le habla a los **directores** por el chat del Centro de Agentes. Cada director
coordina a sus subagentes creando tareas en la cola (`/api/agentes`).

**Director de Marketing** → `investigacion`, `contenido` (content-creator), `creativo`
(creative-designer), `programador`, `metricas`, `ads` (meta-ads-analyst).

**Director Comercial** → `sdr`, `calificacion`, `agenda`, `crm`, `propuestas`.

**Director de Desarrollo** → `relevador`, `planificador`, `desarrollador`, `revisor`,
`qa`, `devops`, `soporte`, `documentador`.

Conexión entre áreas (vía la plataforma/Supabase): Marketing avisa señales de intención a
Comercial; Comercial pasa objeciones a Marketing y requerimientos ganados a Desarrollo;
Desarrollo devuelve casos con métricas a Marketing/Comercial.

> El MCP `meta-ads` se configura en `.mcp.json` (token en `.env`, ignorado por git).

## Nota de runtime (a alinear)
El doc pide agentes en **Python** (n8n solo como trigger). Hoy estos están definidos como
subagentes de Claude Code sobre el plan (polling invertido). Las definiciones `.md` sirven de
spec para cualquier runtime; la decisión Python vs Claude Code queda abierta.

## Restricción técnica (heredada del funnel)

- Motor = **scheduled cloud agent sobre el plan de Claude**, NUNCA la API de Anthropic.
- Polling invertido: la plataforma encola; Claude consume y devuelve por endpoint
  (`POST /api/crm/external/...`, `X-API-Key`, upsert idempotente).

## Estado del sistema

Ver `vibe/estado.md` para qué está definido y qué falta. El gran desbloqueante hoy
es **llenar los `[POR DEFINIR]`** en la reunión de equipo (ver `REUNION.md`).
