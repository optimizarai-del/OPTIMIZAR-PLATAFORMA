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

## Configuración base (ICP)
- Rubro objetivo: estudios contables/impositivos (nicho ancla, mejor prueba social), estudios jurídicos,
  consultoras y PyMEs de servicios con procesos administrativos pesados.
- Tamaño de empresa: PyME ~5–50 empleados, ya facturando bien, con volumen de procesos manuales
  (ej. estudios con 100+ clientes).
- Cargo objetivo: socio / dueño / director / socio administrador (en estudios, el socio a cargo de la operación).
- Geografía: Argentina (escalable a LATAM).
- Idioma: español.
- Cupo diario de envíos: 20–30/día objetivo. WARM-UP: arrancar 10–15/día la semana 1 y escalar gradual.

## ⛔ EXCLUSIÓN DURA (contractual — NO negociable)
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

## Gotchas descubiertos
- Lorenzo y Asociados (red nacional, sede en Bella Vista BA) lista una sucursal "Santa Rosa" — ante la duda se descartó; verificar si esa Santa Rosa es La Pampa antes de incluirlos.
- Tres de cinco emails encontrados son buzones genéricos (estudio@, info@, contacto@). Para estudios más chicos los emails personales de socios aparecen en la web; para estudios con red/alianzas no siempre.
- Disparador transversal más potente identificado: temporada DDJJ Ganancias/Bienes Personales período 2025, vencimiento extendido a julio 2026 (RG ARCA 5851/2026) — todos los estudios contables en pico de carga.
- [2026-06-12] Estudio Varese (Martínez, GBA, desde 1960): no publica nombres de socios. Candidato para corrida futura con investigación adicional (LinkedIn/CPCE).
- [2026-06-12] Martínez Cataldi y Asociados (CABA, Coghlan): tampoco publica socios. Email funcional pero sin nombre para personalizar. Reservar para corrida futura.
- [2026-06-12] En estudios con equipo grande (del Amo, 7+ profesionales), el ángulo "multiplicador" funciona mejor que el de "ahorro de horas de un solo contador".

## Estado actual de la tarea
- [x] Fase 1 — agentes listos
- [x] Fase 2 — backend (en rama equipo-ventas)
- [x] Bloque A — ICP + oferta definidos
- [x] Primera corrida borrador completada (2026-06-11)
- [x] Segunda corrida borrador completada (2026-06-12) — CABA/GBA, 5 leads
- [ ] Migración de columnas en BD de prod (ALTER)
- [ ] Fase 5 (n8n) — envío + escucha
- [ ] Fase 4 — UI chat/seguimiento
- [ ] Fase 3 — scheduled agent diario

## Última corrida
**Fecha:** 2026-06-12 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — CABA + GBA (Buenos Aires)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 5
**Emails personales verificados:** 2 (kevin@estudiosaied.com.ar, fdelamo@estudiodelamo.com)
**Emails genéricos:** 3 (Lutenberg, Suárez, Piacentini — con nombre de contacto)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026)
**Archivos:**
- `funnel/leads/new/borrador-2026-06-12.jsonl` — 5 leads con emails
- `funnel/reportes/2026-06-12.md` — reporte completo
**Próximo bloqueante:** Backend/n8n para envío real. Validar emails antes de activar.

## Corrida anterior (2026-06-11)
**Segmento:** Estudios contables/impositivos — Córdoba Capital + Rosario (Santa Fe)
**Cupo usado:** 5 leads (lote chico, primera corrida)
**Leads encontrados:** 5 | **Descartados:** 1 (Lorenzo y Asociados — precaución La Pampa)
**Archivos:** `borrador-2026-06-11.jsonl` / `reportes/2026-06-11.md`
