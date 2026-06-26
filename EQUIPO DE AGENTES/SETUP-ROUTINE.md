# Setup — Orquestador en vivo (routine de Claude Code)

Para que el orquestador responda solo en el **Centro de Agentes** de la plataforma, hay que
crear una routine de Claude Code (cloud agent disparable) y conectarla con una env.

Mismo patrón que el funnel de ventas (`EQUIPO DE VENTA Y PROSPECCION`), pero para el
canal `agentes`.

## Paso 1 — Crear la routine

Creá una routine de Claude Code (vía `/schedule` o el panel de routines) sobre el repo
**OPTIMIZAR-PLATAFORMA**, con working dir en esta carpeta (`EQUIPO DE AGENTES/`), y este
prompt de arranque:

```
Sos el ORQUESTADOR del equipo de agentes de OPTIMIZAR.
Leé .claude/agents/orquestador.md y seguí sus instrucciones al pie.
Leé el cerebro de marca en vibe/ antes de actuar.

Vas a recibir un mensaje con:
  CANAL=agentes
  API_BASE=<url backend>
  API_KEY=<clave externa>
  MENSAJE: <lo que escribió el humano>

Tu ciclo:
1. Leé el chat: GET {API_BASE}/api/agentes/external/chat?limit=30  (header X-API-Key: {API_KEY})
2. Identificá los mensajes del humano sin responder.
3. Decidí qué subagente(s) hacen falta y creá tareas:
   POST {API_BASE}/api/agentes/external/tareas
4. Respondé al humano en el chat:
   POST {API_BASE}/api/agentes/external/chat
5. Lo sensible (publicar, gastar, enviar) → requiere_aprobacion: true.

No inventes datos. Respetá vibe/ (tono, ICP, oferta, líneas rojas).
```

Al crearla obtenés un **trigger id** y una **fire URL** del tipo:
`https://api.anthropic.com/v1/claude_code/routines/<trig_xxx>/fire`

## Paso 2 — Conectar la env en EasyPanel

Agregá al backend (las otras ya las tenés del funnel):

```
CLAUDE_ORQUESTADOR_FIRE_URL=https://api.anthropic.com/v1/claude_code/routines/<trig_xxx>/fire
```

> Si NO la setean, el sistema usa `CLAUDE_ROUTINE_FIRE_URL` como fallback — pero esa apunta
> al chat-responder del CRM, así que para el orquestador conviene su propia routine.

## Paso 3 — Probar
En la plataforma → Centro de Agentes → escribile algo. El backend dispara la routine,
el orquestador lee el chat, reparte tareas y responde. Lo ves en el chat + el feed de tareas.

## Subagentes
Cada subagente puede ser su propia routine (que pollea `tareas/pending?agente=<rol>`) o
correr dentro del ciclo del orquestador. Empezá con el orquestador + 1 subagente (ej. `ads`,
que ya tiene el token de Pipeboard) y sumá el resto.
