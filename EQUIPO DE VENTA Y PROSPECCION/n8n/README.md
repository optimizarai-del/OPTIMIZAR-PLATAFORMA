# n8n — Workflows del Equipo de Venta y Prospección

n8n es **el transporte**: no busca ni escribe (eso lo hacen los agentes de Claude Code).
Solo **dispara** los correos ya escritos y, más adelante, **escucha** las respuestas.

## Workflow 1 — Envío (`workflow-1-envio.json`)
Lee del CRM los leads con email ya escrito y los manda por SMTP de Hostinger, uno por vez
con espera entre envíos (warm-up), y marca cada uno como `enviado` + etapa `contactado`.

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
2. Cargá un lead de prueba con email tuyo y mensaje escrito (vía `POST /api/crm/external/oportunidades`
   con `outreach_status:"escrito"`, `mensaje_asunto`, `mensaje_cuerpo`, `contacto_email`).
3. En n8n, abrí el workflow y tocá **"Test workflow"**. Debería: traer el lead, mandarte el mail,
   y marcarlo `enviado`. Verificá que llegó y que en el CRM quedó en etapa `contactado`.

### Deliverability (no negociable para fríos)
- En hPanel verificá **SPF** y **DKIM** del dominio (Hostinger los trae; confirmá que estén activos).
- Considerá un registro **DMARC** en `p=none` para empezar a monitorear.
- Respetá el warm-up: 10–15/día la semana 1; subí gradual hasta 20–30.
- El nodo "Esperar" (90s) espacia los envíos para no disparar filtros de spam.

## Workflow 2 — Escucha de respuestas (pendiente)
Se arma después de validar el envío. Gmail/IMAP trigger sobre respuestas → clasifica →
`POST /api/crm/external/oportunidades` con `outreach_status:"respondido"` + `respuesta_recibida`,
y `inbox-responder` borradorea la contestación.
