# stack.md — Stack técnico de herramientas (del doc Vibe Marketing)

> Qué herramienta usa cada agente. Sobre infraestructura que OPTIMIZAR ya tiene operativa.

## General
- **Runtime de agentes:** Claude Code sobre el plan Max (scheduled cloud agents / routines).
- **Modelos:** Claude (principal) + OpenAI / Gemini según tarea.
- **Base de datos / memoria:** Supabase (PostgreSQL + pgvector).
- **Infra:** Hostinger VPS + Easypanel.
- **Scheduler / triggers:** n8n (solo como disparador externo; la lógica vive en los agentes).

## Herramientas por agente

### Marketing
| Agente | Herramientas |
|--------|--------------|
| Investigador | Playwright + Google Trends + Claude |
| Contenido | Claude + archivos `vibe/` |
| Creativo | **ChatGPT Images (OpenAI)** (imágenes) + **Higgsfield** (video/reels) + `brand.md` |
| Programador | Instagram Graph API + LinkedIn API + n8n (scheduler) |
| Métricas | Meta API + LinkedIn API + Supabase |
| Meta Ads (extra) | Pipeboard (Meta Ads MCP) — token ya configurado |

### Comercial
| Agente | Herramientas |
|--------|--------------|
| SDR | Apollo + Instantly + Claude + `icp.md` |
| Calificador | WhatsApp API (WATI) + Instagram DM + Claude + `icp.md` |
| Agenda | Google Calendar + n8n |
| CRM | Supabase + Notion + n8n |
| Propuestas | Claude + `oferta.md` + `casos.md` + `icp.md` |

### Desarrollo
| Agente | Herramientas |
|--------|--------------|
| Relevador | Requerimientos + Servicios (plataforma) + `ai_service` |
| Planificador | Proyectos + Tareas (plataforma) + `ai_service` |
| Desarrollador | GitHub + Claude Code |
| Revisor | Claude Code (code review) |
| QA | Claude Code |
| DevOps | EasyPanel + Bash |
| Soporte | Logs + Supabase + CRM |
| Documentador | Drive + Claude Code |

## Cuentas / credenciales para operar a pleno
- **Ya:** Claude Max, Supabase, Hostinger VPS+Easypanel, Hostinger Email (SMTP/IMAP), Pipeboard,
  Google (Calendar/Drive)+Notion (MCP), GitHub, Meta Business.
- **Faltan abrir:** OpenAI (imágenes), Higgsfield (video/reels), Apollo, Instantly, WhatsApp WATI,
  app Meta for Developers (Instagram Graph), app LinkedIn Developers.
