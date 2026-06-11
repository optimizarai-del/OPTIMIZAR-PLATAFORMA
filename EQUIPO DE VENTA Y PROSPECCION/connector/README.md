# Puente de Chat — conectar tu plan Claude Max al chat de la plataforma

Hace que el **orquestador responda en el chat de la plataforma OPTIMIZAR**, en vivo, usando tu
**plan Max** (sesión iniciada), sin API de Anthropic. La plataforma es la interfaz; este puente
es el cerebro que corre sobre tu plan.

## Cómo funciona
```
[Vos escribís en la plataforma]  →  chat (Postgres)  ←  [Claude Code en loop, logueado a tu Max]
                                                          lee mensajes nuevos → responde como orquestador
```
El puente es un loop de Claude Code que cada minuto:
1. Lee el chat: `GET {API_BASE}/api/crm/external/chat` con header `X-API-Key`.
2. Detecta mensajes con `rol:"humano"` que NO tienen un mensaje de `rol:"agente"` posterior.
3. Responde como el orquestador (lee el CRM y `funnel/estado.md` para contexto real).
4. Postea la respuesta: `POST {API_BASE}/api/crm/external/chat` con `{ "contenido": "..." }`.

## Requisitos
- Claude Code instalado y **logueado con tu cuenta del plan Max** en la máquina donde corra
  (tu PC, o mejor un server siempre encendido — así funciona aunque apagues la compu).
- Variables: `API_BASE` (URL del backend) y `API_KEY` (= `EXTERNAL_API_KEY` del backend).

## Cómo levantarlo
1. Cloná el repo en el server y entrá a `EQUIPO DE VENTA Y PROSPECCION/`.
2. Logueá Claude Code a tu plan: `claude` (la primera vez te pide iniciar sesión con tu cuenta Max).
3. Exportá las variables y lanzá el loop:
   ```bash
   export API_BASE="https://TU-BACKEND.easypanel.host"
   export API_KEY="<EXTERNAL_API_KEY del backend>"
   claude
   ```
   Y dentro de Claude Code, pegá:
   ```
   /loop 1m Sos el funnel-orchestrator. Conectate al chat de la plataforma OPTIMIZAR.
   1) GET $API_BASE/api/crm/external/chat (header X-API-Key: $API_KEY) — trae los últimos mensajes.
   2) Encontra los mensajes con rol "humano" que todavia no tengan una respuesta de rol "agente" posterior.
   3) Para cada uno: respondé como el orquestador del Equipo de Venta y Prospeccion, claro y breve,
      leyendo funnel/estado.md y, si hace falta, el CRM (GET $API_BASE/api/crm/stats con X-API-Key)
      para datos reales. Si el humano pide algo que requiere aprobacion o una accion del equipo, decilo.
   4) Posteá cada respuesta con POST $API_BASE/api/crm/external/chat
      body {"contenido":"<tu respuesta>"} header X-API-Key: $API_KEY.
   5) Si no hay mensajes sin responder, no hagas nada.
   ```

## Notas
- El `/loop 1m` revisa cada minuto → respuestas casi en vivo mientras el puente esté corriendo.
- Para que ande 24/7 con la PC apagada, corré esto en un server/VPS siempre encendido logueado a tu Max.
- Mientras el puente esté caído, los mensajes quedan guardados; cuando vuelve, los responde.
- Esto NO usa la API de Anthropic: corre sobre tu plan, por login.
