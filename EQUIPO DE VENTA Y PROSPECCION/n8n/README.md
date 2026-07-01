# n8n — Workflows del Equipo de Venta y Prospección (FALLBACK)

> ⚠️ **El envío y la escucha ahora se hacen EN CÓDIGO** dentro del backend
> (`backend/app/outreach_service.py` + `scheduler.py`), reutilizando el SMTP que ya está
> configurado y sin dependencias externas. Estos workflows de n8n quedan como **alternativa
> no-código / fallback** por si algún día se quiere mover fuera del backend. Para la operación
> normal **no hace falta importar nada de acá** — solo configurar las variables `OUTREACH_*`
> e `IMAP_*` en el `.env` y poner `OUTREACH_ENABLED=true`.

n8n es **el transporte**: no busca ni escribe (eso lo hacen los agentes de Claude Code).
Solo **dispara** los correos ya escritos y **escucha** las respuestas.

## Workflow 1 — Envío (`workflow-1-envio.json`)
Lee de **Contactos** los leads con mensaje ya escrito (`estado='escrito'`) y los manda por SMTP
de Hostinger, uno por vez con espera entre envíos (warm-up), y marca cada uno como `contactado`.
El contacto queda en la base de Contactos; solo sube al pipeline si responde.

```
Cada día 9hs → Obtener pendientes (GET outbox) → Separar leads → Loop 1x1
   → Enviar email (SMTP Hostinger) → Marcar enviado (POST upsert) → Esperar 90s → (loop)
```

### Cómo importarlo
1. En n8n: **Workflows → Import from File** → elegí `workflow-1-envio.json`.
2. **Crear credencial SMTP** (Hostinger):
   - Host: `smtp.hostinger.com` · Puerto: `465` · SSL: ON
   - User: tu email completo (ej. `info@tudominio.com`) · Password: la del buzón (hPanel → Emails)
   - Asignala al nodo **"Enviar email"**.
3. **Reemplazar placeholders** en los 2 nodos HTTP ("Obtener pendientes" y "Marcar enviado"):
   - `https://API_BASE` → la URL real de tu backend (ej. `https://tu-dominio-de-la-plataforma`).
   - `API_KEY_AQUI` → el valor de `EXTERNAL_API_KEY` del `.env` del backend.
   - Tip: en vez de pegar la key en cada nodo, podés crear una credencial **Header Auth**
     (Name: `X-API-Key`, Value: tu key) y usarla en ambos nodos con Authentication = Header Auth.
4. En el nodo **"Enviar email"** poné el `fromEmail` real (ej. `OPTIMIZAR <info@tudominio.com>`).

### Cómo probarlo (1 lead de prueba)
1. Asegurate de que el backend tenga `EXTERNAL_API_KEY` configurada y la migración de columnas aplicada.
2. Cargá un lead de prueba con email tuyo y mensaje escrito (vía `POST /api/crm/external/contactos`
   con `estado:"escrito"`, `mensaje_asunto`, `mensaje_cuerpo`, `email`).
3. En n8n, abrí el workflow y tocá **"Test workflow"**. Debería: traer el lead, mandarte el mail,
   y marcarlo `enviado`. Verificá que llegó y que en el CRM quedó en etapa `contactado`.

### Deliverability (no negociable para fríos)
- En hPanel verificá **SPF** y **DKIM** del dominio (Hostinger los trae; confirmá que estén activos).
- Considerá un registro **DMARC** en `p=none` para empezar a monitorear.
- Respetá el warm-up: 10–15/día la semana 1; subí gradual hasta 20–30.
- El nodo "Esperar" (90s) espacia los envíos para no disparar filtros de spam.

## Workflow 2 — Escucha de respuestas (`workflow-2-escucha.json`)
Escucha el inbox por IMAP de Hostinger; cuando llega una respuesta, extrae el email y el texto,
y se lo registra al CRM (matchea el lead por email).

```
Inbox IMAP (nuevo mail) → Extraer email + texto → ¿Tiene email? → Registrar respuesta (POST)
```
El backend (`POST /api/crm/external/respuesta`) busca el **contacto** por email, lo marca
`estado="respondido"`, guarda el texto y lo **promueve al pipeline** (crea una Oportunidad en
etapa `contactado`). Después, el agente `inbox-responder` clasifica y borradorea la contestación.

### Cómo importarlo
1. n8n → **Import from File** → `workflow-2-escucha.json`.
2. **Crear credencial IMAP** (Hostinger) y asignarla al nodo "Inbox IMAP":
   - Host: `imap.hostinger.com` · Puerto: `993` · SSL: ON
   - User: tu email completo · Password: la del buzón.
3. Reemplazar `https://API_BASE` y `API_KEY_AQUI` en el nodo "Registrar respuesta" (igual que el WF1).
4. **Activá** el workflow (toggle "Active") para que escuche en tiempo real.

### Notas
- El nodo "¿Tiene email?" descarta correos sin remitente válido (autoresponders raros, etc.).
- Para no procesar correos viejos, en la credencial/nodo IMAP filtrá por no leídos (UNSEEN) — es el default.
- El matcheo es por email del remitente. Si un lead responde desde otra dirección, no matchea (queda sin registrar).
