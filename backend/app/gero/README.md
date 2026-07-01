# Gero — asistente IA de OPTIMIZAR en WhatsApp

Gero atiende a los clientes/prospectos por **WhatsApp**, tiene **memoria** en la base de
datos, usa **Anthropic** como cerebro interno y opera el **CRM**: carga prospectos, los
clasifica, les deja notas y ofrece agendar una reunión por **Calendly**.

> ⚠️ **Por qué Gero sí usa la API de Anthropic** (a diferencia del resto de los agentes, que
> corren sobre routines de Claude Code): necesita **responder en tiempo real** al webhook de
> WhatsApp. Es la misma excepción documentada que ya usa `ai_service.py`. No usa API para el
> resto de las áreas — solo Gero, y solo para conversar.

## Arquitectura

```
WhatsApp ⇄ YCloud ⇄  POST /api/gero/webhook  ─►  cerebro.responder()
                                                     │
                          ┌──────────────────────────┼───────────────────────────┐
                          ▼                          ▼                            ▼
                  memoria (DB)              Anthropic (tool-use)            herramientas → CRM
             gero_conversaciones            claude-haiku-4-5          guardar/clasificar/nota/
             gero_mensajes                                            calendly/handoff
                                                     │
                                                     ▼
                                     enviar_whatsapp() ─► YCloud ─► cliente
```

### Archivos (`backend/app/gero/`)
| Archivo | Rol |
|---|---|
| `personalidad.py` | System prompt + identidad de Gero (tono tipo Tomi de Sonner) y el link de Calendly. |
| `herramientas.py` | Las 5 tools (function calling) que tocan el CRM + sus ejecutores. |
| `ycloud.py` | Transporte WhatsApp: enviar mensajes, parsear el webhook, validar el token. |
| `cerebro.py` | Loop de conversación con Anthropic (tool-use) + memoria en DB. |
| `routers/gero.py` | Endpoints: webhook, prueba, observabilidad. |

### Tablas (memoria)
- **`gero_conversaciones`** — una por número de WhatsApp (`wa_id`), con vínculo al `Contacto`
  del CRM, `estado` (activa/pausada/handoff_humano/cerrada), `nivel_interes` y un `resumen` rodante.
- **`gero_mensajes`** — historial completo de cada turno (user/assistant) + traza de tools.

Se crean solas al arrancar el backend (`Base.metadata.create_all`).

## Herramientas de Gero (CRM)
| Tool | Qué hace |
|---|---|
| `guardar_prospecto` | Crea/actualiza un `Contacto` (origen `whatsapp`, idempotente por `wa:<wa_id>`). |
| `clasificar_prospecto` | Marca el interés: `frio` / `tibio` / `caliente`. |
| `agregar_nota` | Deja observaciones para el equipo en `Contacto.info` (con timestamp). |
| `compartir_calendly` | Marca al prospecto caliente y devuelve el link de agenda. |
| `handoff_humano` | Escala la charla: pausa a Gero y avisa en el chat de la plataforma (canal `agentes`). |

## Configuración (`.env`)
```
ANTHROPIC_API_KEY=...            # ya existente; el cerebro de Gero
YCLOUD_API_KEY=...               # ycloud.com → API Keys
GERO_PHONE_NUMBER=549341...      # número de WhatsApp Business (E.164 sin '+')
YCLOUD_WEBHOOK_SECRET=...        # token para validar el webhook (recomendado)
CALENDLY_URL=https://calendly.com/optimizar-ai/30min
GERO_MODEL=claude-haiku-4-5-20251001   # opcional
```

### Configurar el webhook en YCloud
Apuntá el webhook de mensajes entrantes a:
```
https://TU-BACKEND/api/gero/webhook?token=<YCLOUD_WEBHOOK_SECRET>
```
(o mandá el token en el header `X-Webhook-Token`). El endpoint responde `200` al toque y
procesa la respuesta en background.

## Probar sin WhatsApp
Con un usuario **manager/admin** (JWT), simulá una charla — no manda nada a WhatsApp, pero sí
persiste memoria y ejecuta las tools del CRM:

```bash
curl -X POST https://TU-BACKEND/api/gero/test \
  -H "Authorization: Bearer <JWT>" -H "Content-Type: application/json" \
  -d '{"wa_id":"5493410000000","texto":"Hola, tienen algo para automatizar WhatsApp?","nombre":"Juan"}'
```

Observabilidad:
- `GET /api/gero/conversaciones` — lista de charlas con estado e interés.
- `GET /api/gero/conversaciones/{id}` — el hilo completo + traza de herramientas.

## Pendiente (próxima tanda)
- Panel en la plataforma (frontend) para ver las conversaciones de Gero.
- Resumen rodante automático (`resumen`) para relaciones muy largas.
- Soporte de multimedia entrante (hoy Gero maneja solo texto).
