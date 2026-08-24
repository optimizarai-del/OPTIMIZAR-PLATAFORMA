# Gero — asistente IA de OPTIMIZAR en WhatsApp

Gero atiende a los clientes/prospectos por **WhatsApp**, tiene **memoria** en la base de
datos, usa **Anthropic** como cerebro interno y opera el **CRM**: carga prospectos, los
clasifica, les deja notas y ofrece agendar una reunión por **Calendly**.

> ⚠️ **Por qué Gero sí usa la API de Anthropic** (a diferencia del resto de los agentes, que
> corren sobre routines de Claude Code): necesita **responder en tiempo real** al webhook de
> WhatsApp. Es la misma excepción documentada que ya usa `ai_service.py`. No usa API para el
> resto de las áreas — solo Gero, y solo para conversar.

## Arquitectura (entra por n8n)

```
WhatsApp ─► YCloud ─► n8n (webhook /optimizar-asistente)
                        │  switch por tipo:
                        │   • texto  → body.text.body
                        │   • audio  → descarga + Whisper (OpenAI) → <audio>…</audio>
                        │   • imagen → descarga + GPT-4o-mini      → <image>…</image>
                        │  → normaliza a { message } → buffer Redis (debounce 15s)
                        ▼
              POST /api/gero/mensaje  (X-API-Key)
                        │
       ┌────────────────┼─────────────────────┐
       ▼                ▼                       ▼
 memoria (DB)   Anthropic (tool-use)     herramientas → CRM
 gero_convers.  claude-haiku-4-5    guardar/clasificar/nota/calendly/handoff
                        │
                        ▼
        devuelve { "respuesta": "...", "enviar": true }
                        │
                        ▼
              n8n envía la respuesta por WhatsApp (nodo YCloud send)
```

Gero **no** manda el mensaje él mismo en este flujo: **devuelve el texto** y n8n lo envía.
(El endpoint `/api/gero/webhook`, que sí envía por su cuenta, queda como alternativa por si
algún día se apunta YCloud directo al backend, salteando n8n.)

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

### Conectar n8n con Gero (flujo principal)
Al final del flujo de n8n (después del debounce de Redis), agregá **dos nodos**:

**1) HTTP Request → Gero** (POST)
```
Method : POST
URL    : https://TU-BACKEND/api/gero/mensaje
Headers: X-API-Key: <EXTERNAL_API_KEY del backend>
Body (JSON):
{
  "telefono": "={{ $('Webhook').item.json.body.whatsappInboundMessage.from }}",
  "nombre":   "={{ $('Webhook').item.json.body.whatsappInboundMessage.customerProfile.name }}",
  "mensaje":  "={{ $('Code in JavaScript5').item.json.message }}",
  "wa_message_id": "={{ $('Webhook').item.json.body.whatsappInboundMessage.wamid }}"
}
```
Devuelve `{ "respuesta": "...", "enviar": true, ... }`.

**2) HTTP Request → YCloud send** (POST) — solo si `enviar` es `true`
```
URL    : https://api.ycloud.com/v2/whatsapp/messages
Headers: X-API-Key: <YCLOUD_API_KEY>
Body (JSON):
{
  "from": "<GERO_PHONE_NUMBER>",
  "to":   "={{ $('Webhook').item.json.body.whatsappInboundMessage.from }}",
  "type": "text",
  "text": { "body": "={{ $json.respuesta }}" }
}
```

### Alternativa: YCloud directo al backend (sin n8n)
Apuntá el webhook de YCloud a `https://TU-BACKEND/api/gero/webhook?token=<YCLOUD_WEBHOOK_SECRET>`
(o header `X-Webhook-Token`). En ese caso Gero envía la respuesta él mismo por YCloud.

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

## Cuando el prospecto viene del diagnóstico

El embudo del diagnóstico (`diagnostico.optimizar-ia.com`) termina en un botón que abre
WhatsApp con el mensaje ya escrito y un código adentro:

    Hola, leí mi diagnóstico y quiero avanzar. Código: zkRo7hvt2Y3R

`gero/diagnostico.py` detecta ese código y le carga a Gero la ficha completa **antes** de
que hable: qué respondió en el formulario, el informe que le entregamos y la calificación
interna. No es una tool a propósito — si el modelo se olvidara de llamarla, el primer
mensaje (el que más pesa) saldría genérico.

El código se busca en **todo el historial** de la conversación, no solo en el último
mensaje: llega en el primero, pero Gero tiene que seguir sabiendo quién es en el turno
veinte.

| Calificación | Qué hace Gero |
|---|---|
| 🟢 verde | Ofrece la reunión temprano, sin dar vueltas. |
| 🟡 amarillo | Resuelve dudas primero, ofrece la reunión cuando se entusiasma. |
| 🔴 rojo | Atiende bien pero no insiste con agendar. |

La calificación es interna y Gero tiene instrucción explícita de no mencionarla nunca, ni
el código ni que tiene una "ficha". Para la persona, simplemente leyó su caso.

**Variante B del test A/B:** esos prospectos escriben para *recibir* el diagnóstico, no
para charlar. Gero les pasa el link de entrada, antes que cualquier otra cosa.

**Exclusión territorial:** si el diagnóstico marcó estudio contable en La Pampa (acuerdo
con Larrañaga y Asociados), Gero no ofrece servicios ni reunión, y escala a un humano si
la persona insiste.

La tabla `diagnosticos` la escribe otro servicio. Comparten base, así que se lee con SQL
directo y no con un modelo de SQLAlchemy: declararlo la metería en el `create_all` de la
plataforma, y dos servicios gestionando el mismo esquema termina mal. Si la tabla no está,
Gero funciona como siempre.

```
DIAGNOSTICO_URL=https://diagnostico.optimizar-ia.com   # opcional, ya trae este default
```

## Pendiente (próxima tanda)
- Panel en la plataforma (frontend) para ver las conversaciones de Gero.
- Resumen rodante automático (`resumen`) para relaciones muy largas.
- Soporte de multimedia entrante (hoy Gero maneja solo texto).
