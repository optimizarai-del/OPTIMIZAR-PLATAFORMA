# Agente WhatsApp Inmobiliaria Boutique — Bloque 1

## Descripción del módulo

Este módulo implementa el núcleo conversacional del agente "Valentina", una asesora virtual que atiende consultas inmobiliarias entrantes por WhatsApp. El agente clasifica intenciones, mantiene contexto de sesión, y orquesta las respuestas de Claude usando el historial de la conversación.

La integración con el canal WhatsApp y los nodos de automatización corren en n8n (fuera de este directorio). Este módulo provee las dos piezas de lógica de negocio que n8n invoca: clasificación de intención y gestión de sesión.

**Stack:** Python 3.11 · Supabase (Postgres + SDK) · Anthropic API (Claude Haiku para clasificación, Claude Sonnet para respuestas)

---

## Estructura de archivos

```
agente-whatsapp-inmobiliaria/
├── system_prompt.txt      # Prompt de sistema que define la personalidad y reglas de Valentina
├── intent_router.py       # Clasificador de intenciones vía Claude tool_use + fallback por keywords
├── session_manager.py     # Capa de persistencia conversacional en Supabase (tabla agent_sessions)
└── schema.sql             # DDL completo: tablas properties, leads, agent_sessions + RLS
```

### `system_prompt.txt`

Define la identidad, el tono y las reglas de comportamiento de Valentina. Incluye instrucciones específicas para cada flujo (búsqueda, visita, contrato, consulta general) y restricciones de negocio (no negociar precios, no inventar propiedades, derivar consultas legales complejas). Se carga en tiempo de ejecución y se pasa como `system` en cada llamada a Claude.

### `intent_router.py`

Clasifica el mensaje entrante del usuario en una de cuatro intenciones:

| Intent | Descripción |
|---|---|
| `buscar_propiedad` | El usuario quiere ver o filtrar propiedades del catálogo |
| `agendar_visita` | El usuario quiere coordinar una visita presencial |
| `generar_contrato` | El usuario quiere iniciar reserva o contrato |
| `consulta_general` | Preguntas sobre precios, zonas, trámites, expensas, etc. |

Implementa dos estrategias en cascada:
1. **Vía API (primaria):** llama a Claude Haiku con `tool_use` forzado (`tool_choice: {type: "tool", name: "clasificar_intencion"}`). El modelo devuelve `intent`, `confidence` y `extracted_data` (zona, tipo_propiedad, presupuesto, etc.).
2. **Fallback por keywords (secundaria):** se activa cuando `ANTHROPIC_API_KEY` no está disponible o la API falla. Usa regex con word boundaries para evitar falsos positivos por substrings. Prioridad: visita > búsqueda > contrato > general.

Umbral de confianza: `CONFIDENCE_THRESHOLD = 0.7`. Por debajo se retorna `consulta_general` como fallback seguro, evitando disparar flujos críticos como `generar_contrato` con clasificaciones ambiguas.

### `session_manager.py`

Clase `SessionManager`: gestiona el ciclo de vida de la sesión conversacional de un número de WhatsApp.

Responsabilidades:
- Cargar o crear la fila en `agent_sessions` al instanciarse
- Detectar y resetear sesiones expiradas (TTL: 24 hs)
- Mantener historial de mensajes (límite: 20 mensajes, FIFO rolling window)
- Acumular `context` con datos extraídos por el router (zona, tipo_propiedad, presupuesto, etc.)
- Construir el payload para Claude (`build_claude_payload`) asegurando que el historial empiece con rol `user`
- Hacer upsert del lead asociado (`upsert_lead`)
- Persistir todo con `save()`

### `schema.sql`

DDL idempotente (`CREATE TABLE IF NOT EXISTS`, `DROP TRIGGER IF EXISTS`). Orden de creación: `properties` → `leads` → `agent_sessions` (respeta FK forward refs).

| Tabla | Propósito |
|---|---|
| `properties` | Catálogo de propiedades. Indexado por tipo, operacion, zona, activa, precio |
| `leads` | Prospectos capturados. Pipeline de etapas: nuevo → calificado → visita_agendada → propuesta → cerrado / perdido |
| `agent_sessions` | Contexto conversacional. Una fila por número E.164, TTL 24 hs |

RLS habilitado en las tres tablas. `agent_sessions` y `leads` bloquean acceso anon. `properties` permite lectura pública de propiedades activas (`activa = true`).

---

## Variables de entorno requeridas

| Variable | Requerida | Descripción |
|---|---|---|
| `ANTHROPIC_API_KEY` | Sí (para clasificación vía API) | API key de Anthropic. Sin ella, el router usa fallback por keywords |
| `SUPABASE_URL` | Sí | URL del proyecto Supabase (ej: `https://xxxx.supabase.co`) |
| `SUPABASE_KEY` | Sí | `service_role` key de Supabase. Bypasea RLS. No exponer en cliente |
| `CLAUDE_MODEL` | No | Modelo para respuestas de Valentina. Default: `claude-sonnet-4-5` |

---

## Flujos principales

### Flujo completo de un mensaje entrante

```
WhatsApp (n8n webhook)
        │
        ▼
SessionManager(wa_phone)      ← carga o crea sesión en Supabase
        │
        ▼
sm.add_message("user", texto)
        │
        ▼
route_intent(texto, historial) ← Claude Haiku tool_use
        │                         (fallback: keywords regex)
        ├─ intent + confidence + extracted_data
        │
        ▼
sm.update_context(extracted_data)
sm.last_intent = intent
        │
        ▼
  ¿intent conocido?
  ┌─────┴──────┐
  │            │
  ▼            ▼
flujo       flujo
específico  consulta_general
(ver abajo) │
            └──────┐
                   ▼
         sm.build_claude_payload(system_prompt)
                   │
                   ▼
         POST /v1/messages (Claude Sonnet)
                   │
                   ▼
         sm.add_message("assistant", reply)
         sm.save()
                   │
                   ▼
         Enviar reply → WhatsApp (n8n)
```

### Flujo: buscar_propiedad

```
route_intent → buscar_propiedad
        │
        ▼
Extraer filtros de extracted_data
(zona, tipo, presupuesto, ambientes, operacion)
        │
        ▼
Query a tabla properties (n8n DB node)
        │
        ├── resultados encontrados → inyectar en contexto del prompt → Claude responde
        └── sin resultados         → Claude ofrece dejar datos de alerta
```

### Flujo: agendar_visita

```
route_intent → agendar_visita
        │
        ▼
¿Hay property_id en extracted_data o context?
        │
        ├── Sí → pedir nombre + email + fecha preferida
        └── No → pedir qué propiedad quiere ver (primero)
                │
                ▼
        Crear/actualizar lead con etapa = "visita_agendada"
        sm.upsert_lead({visita_fecha, visita_direccion, property_id})
                │
                ▼
        Claude confirma datos y horario al usuario
```

### Manejo de sesión expirada

```
SessionManager._load()
        │
        ▼
¿expires_at <= now()?
        │
        ├── Sí → reset() (limpia messages, context, last_intent) → nueva conversación
        └── No → carga el estado existente
```

---

## Deuda técnica — BUG-004 / BUG-005 / BUG-006 (para próximo ciclo QA)

Estos tres ítems fueron identificados durante el QA del Bloque 1 y quedan pendientes para el siguiente ciclo. No están implementados en el código actual.

### BUG-004 — Acumulación de filas expiradas en `agent_sessions`

**Descripción:** El método `SessionManager._load()` detecta sesiones expiradas y llama a `reset()` para reutilizar la fila, pero no elimina filas de números que nunca volvieron a escribir. Con volumen alto de leads únicos, la tabla crece indefinidamente.

**Impacto:** Degradación de performance en queries sin índice sobre `expires_at` + costo de almacenamiento en Supabase.

**Fix propuesto:** Activar `pg_cron` en Supabase y schedulear el job indicado en el comentario del código:
```sql
SELECT cron.schedule(
  'purge_expired_sessions',
  '0 * * * *',
  $$DELETE FROM agent_sessions WHERE expires_at < now()$$
);
```
El comentario ya está en `session_manager.py` línea 58. Requiere habilitar la extensión `pg_cron` en el dashboard de Supabase.

---

### BUG-005 — El fallback de keywords no extrae `extracted_data`

**Descripción:** Cuando `route_intent` cae en `_fallback_intent()` (API no disponible o error de red), devuelve siempre `extracted_data: {}`. El router basado en keywords detecta la intención pero no extrae zona, tipo, presupuesto ni ningún otro dato del mensaje.

**Impacto:** El `SessionManager.context` no se actualiza con datos del mensaje cuando se usa el fallback, lo que obliga a Valentina a re-preguntar datos que el usuario ya mencionó en el primer mensaje.

**Fix propuesto:** Agregar extracción básica por regex en `_fallback_intent()` para al menos zona (lista de barrios conocidos) y tipo de propiedad (keywords ya presentes en `busqueda_kw`).

---

### BUG-006 — `build_claude_payload` no incluye el contexto acumulado en el prompt

**Descripción:** `build_claude_payload()` pasa el `system_prompt` tal cual, sin inyectar el `context` acumulado de la sesión (zona buscada, presupuesto, tipo de propiedad, etc.). Ese contexto se guarda correctamente en Supabase pero Claude no lo recibe explícitamente — solo puede inferirlo del historial de mensajes.

**Impacto:** Si el historial fue truncado (rolling window de 20 mensajes) o el usuario mencionó el dato en un mensaje lejano, Claude puede perder el contexto y re-preguntar preferencias ya capturadas.

**Fix propuesto:** Inyectar el contexto al final del system prompt como bloque `## Contexto del lead` antes de construir el payload:
```python
def build_claude_payload(self, system_prompt: str, new_user_message: str | None = None) -> dict:
    context_block = ""
    if self.context:
        context_block = "\n\n## Contexto del lead (datos ya recopilados)\n"
        context_block += "\n".join(f"- {k}: {v}" for k, v in self.context.items())
    full_system = system_prompt + context_block
    ...
```
