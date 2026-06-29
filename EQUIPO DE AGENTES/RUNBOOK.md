# RUNBOOK — Centro de Agentes (orquestación desde la plataforma)

Cómo opera el equipo de IA de OPTIMIZAR, manejado desde la plataforma.

## Quién es quién (rol en la cola ↔ archivo del agente)

| `agente` (cola) | Archivo | Estado |
|-----------------|---------|--------|
| `orquestador`   | `.claude/agents/orquestador.md` | ✅ punto de entrada |
| `investigacion` | `.claude/agents/investigacion.md` | ✅ listo |
| `contenido`     | `.claude/agents/contenido.md` | ✅ listo (publicar necesita tokens IG/LinkedIn) |
| `creativo`      | `.claude/agents/creativo.md` | ✅ listo (OpenAI imágenes + Higgsfield video) |
| `ads`           | `.claude/agents/meta-ads-analyst.md` | ✅ listo (token Pipeboard cargado) |
| `sdr`           | `.claude/agents/sdr.md` | ✅ listo (envío real necesita Apollo/Instantly) |
| `calificacion`  | `.claude/agents/calificacion.md` | ⚠️ necesita WhatsApp + Calendar |
| `crm`           | `.claude/agents/crm.md` | ✅ listo |

## Flujo

```
Humano ──chat──► Orquestador ──crea tareas──► Subagentes ──MCPs──► resultado
  ▲                   │                                              │
  └───── reporta ◄─────┴──────────── sintetiza ◄─────────────────────┘
```

1. El humano escribe en el **chat del Centro de Agentes** (canal `agentes`).
2. La plataforma dispara al **orquestador** (Claude Code sobre el plan, NO API de Anthropic).
3. El orquestador lee el chat, lee `vibe/`, y **crea tareas** para los subagentes.
4. Cada subagente **consume sus tareas pendientes** por polling, las ejecuta con sus MCPs
   y **devuelve el resultado**.
5. El orquestador **sintetiza y responde** en el chat. Lo sensible pide aprobación.

## Endpoints (todos con `X-API-Key` salvo los de UI con JWT)

| Quién | Método | Endpoint |
|-------|--------|----------|
| Orquestador lee chat | GET | `/api/agentes/external/chat?limit=30` |
| Orquestador responde | POST | `/api/agentes/external/chat` |
| Orquestador crea tarea | POST | `/api/agentes/external/tareas` |
| Subagente pide trabajo | GET | `/api/agentes/external/tareas/pending?agente=<rol>` |
| Subagente devuelve | PATCH | `/api/agentes/external/tareas/<id>` |
| UI lista tareas | GET | `/api/agentes/tareas` |
| UI catálogo | GET | `/api/agentes/catalogo` |

## Disparo (fire)
- El humano postea → la plataforma llama `_fire_orquestador` → routine de Claude Code.
- Env: `CLAUDE_ORQUESTADOR_FIRE_URL` (o cae a `CLAUDE_ROUTINE_FIRE_URL`), `CLAUDE_ROUTINE_TOKEN`,
  `SELF_API_BASE`, `EXTERNAL_API_KEY`.
- Si no está configurado, el chat funciona como **buzón**: lo levanta el ciclo programado.

## Restricción
Todo corre **sobre el plan de Claude** (scheduled cloud agents / routines), **nunca la API
de Anthropic** para generación. Polling invertido: la plataforma encola, Claude consume.

## Pendiente de credenciales (para operar a pleno)
- **Publicar contenido:** tokens Instagram Graph + LinkedIn.
- **Calificación:** WhatsApp (WATI) + Google Calendar.
- **SDR envío real:** Apollo + Instantly.
- **Fire en vivo:** setear `CLAUDE_ORQUESTADOR_FIRE_URL` en EasyPanel (si no, modo buzón).
