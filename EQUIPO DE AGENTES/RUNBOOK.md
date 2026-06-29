# RUNBOOK — Equipo de IA de OPTIMIZAR (3 Directores)

Cómo opera el equipo de IA, manejado desde la plataforma. **3 routines = 3 Directores.**
Cada Director es el punto de entrada de su canal de chat y orquesta a SUS subagentes
**en-proceso con la herramienta `Task`** (no hay polling entre agentes, no hay orquestador).

## Arquitectura

```
Humano ──chat (canal X)──► Director X (routine, opus)
                              │  abre subagentes con Task (en paralelo)
                              ▼
                     Subagente A   Subagente B   Subagente C   ...
                              │            │            │
                              └── devuelven resultado ──┘
                              │
                     Director sintetiza ──► responde en el chat
                                         └► encola tareas (visibilidad + aprobación)
```

- **Director = routine.** Subagente = `Task` adentro del Director. Routine extra solo para
  trabajo recurrente con su propia cadencia (funnel diario, métricas diarias, revisar-inbox).
- Los subagentes reciben su tarea **en el prompt** que les pasa el Director y **devuelven el
  resultado** como su mensaje final. NO consultan la cola.
- La **cola de la plataforma** se usa para **visibilidad en la UI + aprobación humana**, no para
  coordinar agentes.

## Los 3 Directores (canal ↔ archivo ↔ clave)

| Canal | Director | Clave de área |
|-------|----------|---------------|
| `marketing`  | `.claude/agents/director-marketing.md`  | `EXTERNAL_API_KEY_MARKETING` |
| `comercial`  | `.claude/agents/director-comercial.md`  | `EXTERNAL_API_KEY_COMERCIAL` |
| `desarrollo` | `.claude/agents/director-desarrollo.md` | `EXTERNAL_API_KEY_DESARROLLO` |

## Equipos (rol en la cola ↔ archivo)

**Marketing:** `investigacion` · `contenido` · `creativo` · `programador` (publicador de redes) ·
`metricas` · `ads` (`meta-ads-analyst.md`, MCP Pipeboard).

**Comercial:** `sdr` · `calificacion` · `agenda` · `crm` · `propuestas`.

**Desarrollo:** `relevador` · `planificador` · `desarrollador` · `revisor` · `qa` · `devops` ·
`soporte` · `documentador`.

## Endpoints (todos con `X-API-Key`)

| Quién | Método | Endpoint |
|-------|--------|----------|
| Director lee su chat | GET | `/api/agentes/external/chat?canal=<área>&limit=30` |
| Director responde | POST | `/api/agentes/external/chat` |
| Director registra tarea (UI) | POST | `/api/agentes/external/tareas` |
| Director actualiza tarea | PATCH | `/api/agentes/external/tareas/<id>` |
| SDR carga lead a Contactos | POST | `/api/crm/external/contactos` |
| Crear/editar oportunidad | POST/PATCH | `/api/crm/external/oportunidades` · `/api/crm/oportunidades/<id>` |
| Ads sync + recomendaciones | POST | `/api/ads/external/sync` · `/api/ads/external/recommendations` |

## Disparo (fire)
El humano postea en un canal → la plataforma llama al fire del Director correspondiente
(`CLAUDE_FIRE_<AREA>` + `EXTERNAL_API_KEY_<AREA>`, con `SELF_API_BASE`). Si no está configurado,
el chat funciona como **buzón** y lo levanta el ciclo programado.

## Restricción
Todo corre **sobre el plan de Claude** (scheduled cloud agents / routines, esfuerzo medio),
**nunca la API de Anthropic** para generación. Modelo: `opus` en todos los agentes.

## Aprobación humana (obligatoria antes de ejecutar)
Publicar contenido · enviar outreach/propuestas · deploy a producción · gasto en ads.
El agente deja el borrador listo y lo encola con `requiere_aprobacion: true`.

## Pendiente de credenciales (para operar a pleno)
- **Imágenes/video:** OpenAI (ChatGPT Images) + Higgsfield (token no-interactivo cloud).
- **Publicar:** Instagram Graph + LinkedIn.
- **Comercial:** Apollo (prospección), Instantly o SMTP (envío), WATI (WhatsApp), Google Calendar.
- **Métricas orgánicas:** Meta API + LinkedIn API. (Meta Ads paga ya anda con Pipeboard.)
