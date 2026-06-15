# Estado Continuo del Funnel — memoria entre corridas

> El `funnel-coo` lee este archivo al inicio de cada ciclo y lo actualiza al final.

## Oferta (lo que va en los emails)
OPTIMIZAR diseña e implementa **sistemas a medida de automatización e IA** que eliminan el trabajo
manual repetitivo en empresas de servicios.
- Software a medida (ej. sistema contable Larrañaga: liquidación de IVA, conciliación bancaria,
  cuentas corrientes, reportes automáticos).
- Agentes de IA (setters, atención, calificación de leads).
- Automatizaciones de procesos (flujos n8n, parsers, integraciones).
- **Prueba social / ángulo:** caso Larrañaga y Asociados — sistema contable real en producción.
- **Mensaje núcleo:** "te hacemos ganar más, ahorrar tiempo y optimizar los procesos que hoy te comen el día".

## El equipo es GENÉRICO — busca el rubro que se le pida
Este equipo prospecta **cualquier tipo de cliente**, no solo contadores. El rubro lo define:
1. una búsqueda encolada desde el formulario "Buscar leads" (`/api/crm/lead-jobs/pending`), o
2. un pedido por el chat ("buscá 5 gimnasios de Rosario"), o
3. si no hay ningún pedido, el **ICP por defecto / ancla** de abajo.
Los pedidos explícitos del humano SIEMPRE mandan sobre el ICP por defecto.

## ICP por defecto / ancla (se usa SOLO si nadie pidió otra cosa)
- Rubro por defecto: estudios contables/impositivos (nicho ancla, mejor prueba social Larrañaga),
  estudios jurídicos, consultoras y PyMEs de servicios con procesos administrativos pesados.
- Tamaño de empresa: PyME ~5–50 empleados, ya facturando bien, con volumen de procesos manuales
  (ej. estudios con 100+ clientes).
- Cargo objetivo: socio / dueño / director / socio administrador (en estudios, el socio a cargo de la operación).
- Geografía: Argentina (escalable a LATAM).
- Idioma: español.
- Cupo diario de envíos: 20–30/día objetivo. WARM-UP: arrancar 10–15/día la semana 1 y escalar gradual.

## ⛔ EXCLUSIÓN DURA (contractual — NO negociable, SOLO contables)
> Aplica únicamente cuando el rubro buscado es estudios contables/impositivos. Otros rubros en La Pampa están permitidos.
- **NO prospectar estudios contables dentro de la Provincia de La Pampa.**
  Exclusividad territorial con Larrañaga y Asociados (cláusula de no competencia).
  El resto del país está libre. Esto es un guardarraíl, no una preferencia: si un lead es un
  estudio contable/impositivo radicado en La Pampa, se DESCARTA sí o sí.

## Personalización mínima recomendada
Nombre, empresa, rubro y un gancho de dolor por rubro.

## Decisiones tomadas
- [2026-06-10] Equipo de agentes creado (Fase 1). Proyecto movido a carpeta propia.
- [2026-06-10] Fase 2 (backend) subida a la rama git `equipo-ventas`.
- [2026-06-11] ICP + oferta definidos (Bloque A). Exclusión La Pampa cargada como guardarraíl.
- [2026-06-11] Primera corrida de búsqueda en MODO BORRADOR. Segmento: estudios contables CABA/GBA/Córdoba/Rosario. 5 leads encontrados, 1 descartado por precaución La Pampa.
- [2026-06-12] Plataforma deployada en producción. Chat en vivo del orquestador funcionando sobre el plan (el backend dispara la routine `chat-responder` al recibir un mensaje). Envío real todavía apagado.
- [2026-06-13] Corrida borrador expandida a Mendoza + Tucumán (NOA). 2 emails personales verificados (Torre-Pulisich, Farina). Descubierto: Xubio lista implementadores en Mendoza con contactos directos — fuente valiosa para próximas corridas.

## Decisiones tomadas (continuación)
- [2026-06-14] Corrida borrador expandida a Salta Capital + Mar del Plata. Salta: Estudio Diéguez (email inferido, ZoomInfo) + Simesen de Bielke (referente NOA >50 años, email de dominio propio). Mar del Plata: Posadas (email personal verificado), Apphatie (sin email), B&R/SMS (genérico, sin nombre). 3 emails escritos, 2 sin contactar.

## Gotchas descubiertos (continuación — 2026-06-15)
- [2026-06-15] GL Estudio (Bahía Blanca): segundo email operativo estudiogl@bvconline.com.ar (BVConline, plataforma de verificación de negocios). Puede ser canal secundario si info@ no responde.
- [2026-06-15] Estudio Vermeulen (Javier Vermeulen, Neuquén + CABA, 2005): email real no extraíble del sitio (contact page 404; formato enmascarado en WebFetch). Candidato para corrida futura vía LinkedIn o CPCE Neuquén.
- [2026-06-15] RS Contadores Neuquén (Belgrano 1216): misma limitación de email enmascarado. Titular no publicado. Candidato corrida futura.
- [2026-06-15] Vaca Muerta angle: Estudio Carnicero confirma nicho de estudios contables especializados en Oil & Gas en Neuquén. Fuente valiosa: Guía Vaca Muerta (guiavacamuerta.com/categorias/estudios-contables.htm). Explorar en corrida dedicada.
- [2026-06-15] CPN Zelarayán (Neuquén): contadoras/contadores independientes sin equipo = CTA de máxima urgencia en temporada pico. Segmento a explorar más en Patagonia.
- [2026-06-15] CPCE Bahía Blanca: publica directorio de matriculados — fuente para corridas futuras en la ciudad (quedan sin cubrir Estudio Villar, Estudio Correa y otros).
- [2026-06-15] CRM stats endpoint (/api/crm/stats) respondió 401 durante la corrida. No bloquea operación pero limita la lectura de métricas de tasa de respuesta. Reportar al equipo de desarrollo.

## Gotchas descubiertos
- Lorenzo y Asociados (red nacional, sede en Bella Vista BA) lista una sucursal "Santa Rosa" — ante la duda se descartó; verificar si esa Santa Rosa es La Pampa antes de incluirlos.
- Tres de cinco emails encontrados son buzones genéricos (estudio@, info@, contacto@). Para estudios más chicos los emails personales de socios aparecen en la web; para estudios con red/alianzas no siempre.
- Disparador transversal más potente identificado: temporada DDJJ Ganancias/Bienes Personales período 2025, vencimiento extendido a julio 2026 (RG ARCA 5851/2026) — todos los estudios contables en pico de carga.
- [2026-06-12] Estudio Varese (Martínez, GBA, desde 1960): no publica nombres de socios. Candidato para corrida futura con investigación adicional (LinkedIn/CPCE).
- [2026-06-12] Martínez Cataldi y Asociados (CABA, Coghlan): tampoco publica socios. Email funcional pero sin nombre para personalizar. Reservar para corrida futura.
- [2026-06-12] En estudios con equipo grande (del Amo, 7+ profesionales), el ángulo "multiplicador" funciona mejor que el de "ahorro de horas de un solo contador".
- [2026-06-13] Implementadores Xubio en Mendoza (Torre-Pulisich, Maipy): ya adoptaron tecnología contable — apertura natural a capa siguiente de automatización. Ángulo sugerido: "ya usás Xubio, OPTIMIZAR es lo que viene después".
- [2026-06-13] Estudio Godoy y Asociados (Tucumán, 30 años): sin nombre de socio publicado. Investigar vía LinkedIn o CPCE de Tucumán antes de activar envío.
- [2026-06-13] Estudios del NOA (Tucumán, Salta, Jujuy) reciben menos propuestas tech que CABA — posible diferenciador en próximas corridas.
- [2026-06-14] Estudio Diéguez (Salta, 11-50 prof.): web devuelve 403, email gdieguez@estudio-dieguez.com.ar inferido vía ZoomInfo. Validar antes del envío real.
- [2026-06-14] Simesen de Bielke (Salta, >50 años): referente NOA en impuestos, ex-presidente CPCE, dictan Posgrado en UNSa. Muy consultados por pares → posible early adopter de tech y multiplicador. Email "administracion@" semi-genérico pero de dominio propio; dirigido a Valeria (2ª gen).
- [2026-06-14] Estudio Apphatie (Mar del Plata, desde 1975, 3 generaciones): muy consolidado pero sin email publicado. CPCE Buenos Aires puede ser fuente para conseguir contacto.
- [2026-06-14] B&R / SMS Latinoamérica (Mar del Plata): perfil corporativo con red regional — posiblemente los socios no son públicos. Investigar vía LinkedIn o SMS Argentina.
- [2026-06-14] Para Salta en general: La Guía Salta lista 20+ estudios pero la mayoría sin web propia. CPCE de Salta puede tener directorio de matriculados con emails. Fuente valiosa para próximas corridas en el NOA.

## Estado del sistema (infra — lo mantiene el equipo de desarrollo, NO lo cambian las corridas)
- Plataforma OPTIMIZAR **deployada en producción** (EasyPanel): CRM + Prospección IA operativos.
- Backend: endpoints externos OK, **migración aplicada**, **chat en vivo sobre el plan funcionando**.
- **Prospección diaria automática: ACTIVA en MODO BORRADOR** (busca y escribe; NO envía nada).
- **Envío real de correos: APAGADO** (`OUTREACH_ENABLED=false`). Encender tras validar emails + warm-up.
- Corridas borrador completadas: 11/06 (Córdoba/Rosario), 12/06 (CABA/GBA), 13/06 (Mendoza/Tucumán), 14/06 (Salta/Mar del Plata), 15/06 (Bahía Blanca/Neuquén) → 25 leads en borrador (3 emails personales verificados, 22 genéricos o inferidos).
- Pendiente real: validar calidad de los emails y, cuando se apruebe, encender el envío (flip a push-vivo).

## Última corrida
**Fecha:** 2026-06-15 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — Bahía Blanca (PBA sur) + Neuquén Capital (Patagonia)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 1 (Lorenzo y Asociados red nacional — precaución La Pampa, mismo caso 11/06)
**Emails escritos:** 5 (todos con email y copy)
**Email status:** 5 genéricos (ningún email personal verificado esta corrida)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) + ángulo Oil & Gas / Vaca Muerta para Neuquén
**Archivos:**
- `funnel/leads/new/borrador-2026-06-15.jsonl` — 5 leads
- `funnel/reportes/2026-06-15.md` — reporte completo
**Total acumulado borrador:** 25 leads (5 corridas)
**Próximo bloqueante:** Backend/n8n para envío real. Validar emails antes de activar.

## Corrida anterior (2026-06-14)
**Fecha:** 2026-06-14 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — Salta Capital + Mar del Plata (PBA interior)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 3
**Emails con copia escrita:** 3 (Diéguez/inferred, Simesen-Bielke/genérico de dominio, Posadas/personal verificado)
**Sin email o sin nombre:** 2 (Apphatie sin email; B&R sin nombre de socio)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026)
**Archivos:**
- `funnel/leads/new/borrador-2026-06-14.jsonl` — 5 leads
- `funnel/reportes/2026-06-14.md` — reporte completo
**Total acumulado borrador:** 20 leads (4 corridas)
**Próximo bloqueante:** Backend/n8n para envío real. Validar emails antes de activar.

## Decisiones tomadas (continuación)
- [2026-06-15] Corrida expandida a Bahía Blanca (hub agroindustrial PBA sur) + Neuquén Capital (Oil & Gas / Vaca Muerta). Nuevo ángulo Oil & Gas para Carnicero (Neuquén). 5 emails escritos, todos genéricos. CRM 5/5 × 200.

## Corrida anterior (2026-06-13)
**Fecha:** 2026-06-13 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — Mendoza Capital + Gran Mendoza + Tucumán (NOA)
**Cupo usado:** 5 leads
**Leads encontrados:** 5 | **Descartados:** 0
**Archivos:** `borrador-2026-06-13.jsonl` / `reportes/2026-06-13.md`

## Corrida anterior (2026-06-12)
**Segmento:** Estudios contables/impositivos — CABA + GBA (Buenos Aires)
**Cupo usado:** 5 leads (lote de expansión metropolitana)
**Leads encontrados:** 5 | **Descartados:** 0
**Archivos:** `borrador-2026-06-12.jsonl` / `reportes/2026-06-12.md`

## Corrida anterior (2026-06-11)
**Segmento:** Estudios contables/impositivos — Córdoba Capital + Rosario (Santa Fe)
**Cupo usado:** 5 leads (lote chico, primera corrida)
**Leads encontrados:** 5 | **Descartados:** 1 (Lorenzo y Asociados — precaución La Pampa)
**Archivos:** `borrador-2026-06-11.jsonl` / `reportes/2026-06-11.md`
