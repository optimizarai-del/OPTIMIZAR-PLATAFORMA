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

## Gotchas descubiertos
- (vacío)

## Estado actual de la tarea
- [x] Fase 1 — agentes listos
- [x] Fase 2 — backend (en rama equipo-ventas)
- [x] Bloque A — ICP + oferta definidos
- [ ] Migración de columnas en BD de prod (ALTER)
- [ ] Fase 5 (n8n) — envío + escucha
- [ ] Fase 4 — UI chat/seguimiento
- [ ] Fase 3 — scheduled agent diario

## Última corrida
- Aún no hubo corridas de búsqueda. ICP listo → próximo bloqueante es la fuente de leads (paso D, n8n).
