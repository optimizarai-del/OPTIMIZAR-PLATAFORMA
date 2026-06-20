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

## Gotchas descubiertos (continuación — 2026-06-20)
- [2026-06-20] Juan Pablo Melnik (Catamarca, CPN Matrículas 1117): Vocal Titular 1 CPCE Catamarca, docente FCE UNCa (carrera CPN), síndico judicial, speaker sobre "Digitalización del Estudio Contable" en CPCE Catamarca (taller reprogramado 2x por demanda). Tiene YouTube propio con contenido de estudio contable digital. Perfil de adoptador temprano idéntico a Rojas Naser ⭐⭐. CANDIDATO PRIORITARIO para encontrar email en corrida futura (vía cpcecat.org.ar comisiones, LinkedIn o YouTube). Ángulo sugerido: "ya enseñás digitalización — OPTIMIZAR es la capa de automatización que le sigue al software".
- [2026-06-20] Marnetto & Brigido (La Rioja Capital, desde 1980): email info@estudiomarnetto.com.ar verificado (dominio propio). Primer estudio de La Rioja Capital en el programa. Servicios: impositivo, contable, legal, agropecuario, proyectos de inversión. Candidato ⭐ para primer envío en La Rioja.
- [2026-06-20] La Rioja Capital tiene baja presencia web de estudios contables. La mayoría usa solo directorios físicos (Licuo, argentino.com.ar) sin sitio propio. Fuentes adicionales para corridas futuras: CPCE La Rioja, Estudio Quijano y Asociados, Estudio José Mario Brizuela (Carmelo Valdez 165), AP Group (San Martin 117 - 5º Piso, ECONNREFUSED hoy).
- [2026-06-20] Catamarca Capital tiene capacidad para 5+ corridas adicionales. Candidatos identificados: Estudio Haddad y Asociados (Rojas 600 — Juan Pablo Haddad CPN, robado en 2019 y siguió operando), Estudio Vega Pedro-Maria (Vicario Segura 782), Estudio Cordoba Mauvecin (República 476), Rivera Michea & Asociados (email pendiente).
- [2026-06-20] CPCE Catamarca (cpcecat.org.ar): sitio activo, publica comisiones con nombres de vocales. Fuente confiable para encontrar emails de profesionales en corridas futuras. Melnik es Vocal Titular 1 → su email probablemente publicado en página de autoridades.
- [2026-06-20] Decisiones tomadas: La Rioja Capital (primera incursión) + Catamarca Capital (primera incursión). Completa el cinturón NOA (Mendoza ✓, Tucumán ✓, Salta ✓, Jujuy ✓, La Rioja ✓, Catamarca ✓). 5/5 × 200 al CRM. Hito: 50 leads en borrador (10 corridas).

## Gotchas descubiertos (continuación — 2026-06-19)
- [2026-06-19] Rojas Naser (Jujuy): CPN speaker sobre Libro de Sueldos Digital en CPCEs de Mendoza, Río Negro, San Luis, La Rioja, Entre Ríos y Jujuy. Usa software ISO 9001. Mentalidad tech consolidada → ángulo "capa siguiente de automatización" mucho más efectivo que el ángulo de dolor estándar. Candidato ⭐⭐ para primer envío real en Jujuy.
- [2026-06-19] Estudio Lasquera (Jujuy): cofundadoras Gabriela Lasquera y Mirta Puente. Email cpnglasquera@estudiolasquera.com.ar verificado (dominio propio). Web en mantenimiento pero email activo. Primer Jujuy del programa.
- [2026-06-19] Alvarenga & Asociados (Posadas, Misiones): primera incursión de OPTIMIZAR en Misiones. Email info@estudioalvarenga.com.ar verificado (dominio propio). Servicio dual laboral + impositivo → ángulo de doble carga.
- [2026-06-19] Grosso Juárez y Asociados (Jujuy): 20+ años, dos socios (D. Grosso y B. Juárez). Sitio estgrossojuarez.com caído (ECONNREFUSED). Email dgrossso@arnet.com.ar inferido desde resultados de búsqueda. Validar antes del envío real vía CPCE Jujuy. Arnet como proveedor sugiere profesional establecido.
- [2026-06-19] Jujuy tiene capacidad para 5+ corridas adicionales. Candidatos para próximas corridas: BMB Estudio Contable & Gestión (Belgrano 775), Estudio M&Co Soluciones Empresariales, Estudio Velazquez, Daniel Hugo Guantay (sin email), Estudio Amerise.
- [2026-06-19] Posadas (Misiones) tiene 20+ estudios en directorio guia-misiones.miguiaargentina.com.ar. Para próximas corridas: Estudio Lindstrom-Ramirez y Asoc. (Jujuy 2126), Zimmermann Estudio Contable y Jurídico (San Lorenzo 1752), Britto Julio C e Hijo, Pretzel y Asociados (Av Lavalle 2634).
- [2026-06-19] Corrientes Capital: segundo intento sin resultados de calidad. Facebook bloquea sin login; CPCE Corrientes no devuelve directorio privado via ACGRA; Páginas Amarillas renderiza vacío. Postergado hasta contar con fuente dedicada (CPCE Corrientes directorio matriculados).
- [2026-06-19] Yellpo.com: dominio en liquidación (redirige a GoDaddy "for sale"). No usar como fuente en corridas futuras.
- [2026-06-19] Decisiones tomadas: Jujuy Capital (primera incursión NOA) + Posadas Misiones (primera incursión NEA/Misiones). 5/5 × 200 al CRM.

## Gotchas descubiertos (continuación — 2026-06-18)
- [2026-06-18] Pronea (Resistencia, Chaco): equipo interdisciplinario CPN + abogados, 20+ años en el NEA. Eduardo Muñoz Manni (CPN). Email propio (info@pronea.com.ar). Candidato ⭐ para primer envío en el NEA — sector con baja exposición a propuestas tech.
- [2026-06-18] Estudio San Cristóbal (Resistencia, Chaco): familia San Cristóbal, 40+ años, segunda generación. Actuación en Chaco y todo el NEA. Daniel San Cristóbal (UNNE 1989) es el socio activo más reciente. Candidato ⭐ para primer envío en el NEA.
- [2026-06-18] Resistencia (Chaco) tiene capacidad para 5+ corridas adicionales. Primer NEA prospectado — mercado poco saturado por propuestas tech. Posibles fuentes futuras: guia-chaco.miguiaargentina.com.ar, licuo.com.ar/resistencia, Páginas Amarillas Resistencia.
- [2026-06-18] Corrientes Capital: múltiples búsquedas sin resultados de calidad (estudios sin sitio web accesible o confundidos con "Av. Corrientes" de CABA). Postergado a corrida futura. Fuente sugerida: CPCE Corrientes (buscar directorio matriculados).
- [2026-06-18] SBS Estudio Jurídico y Contable (San Juan): nombre de socio no publicado en el sitio. Investigar vía cpcesj.org.ar (tiene sección "consulta de asesor") o LinkedIn antes del envío real. Email Gmail → deliverability más baja que dominios propios.
- [2026-06-18] Lescuras & Asoc. (San Juan, 48+ años, 300+ clientes): contacto solo por WhatsApp/teléfono, sin email publicado. Candidato de alta calidad para corrida futura con investigación adicional (cpcesj.org.ar o LinkedIn).
- [2026-06-18] cpnmapsa.com (Estudio Manrique-Palacio-Saball, San Juan): ECONNREFUSED. Candidato para corrida futura cuando el sitio esté accesible.
- [2026-06-18] Decisiones tomadas: San Juan Capital + Resistencia/Chaco (NEA primera incursión). 5/5 × 200 al CRM.

## Gotchas descubiertos (continuación — 2026-06-17)
- [2026-06-17] Bisonni Estudio Contable (Rosario): único estudio del programa que ofrece Business Intelligence + tableros de control como servicio. También criptos y activos digitales. Email personal (daniel.bisonni@hotmail.com.ar). Candidato ⭐⭐ para primer envío real.
- [2026-06-17] Estudio Pereiro Pereiro (Rosario): única especialización en recupero IVA exportadores del programa. Si convierte, abre segmento "estudios con clientes comex" para corridas futuras (Avellaneda 1435, gustavopereiro@hotmail.com).
- [2026-06-17] Contadores Rosario (Pablo Morales): certificación ISO 9001:2015 — rara en el sector. Primera empresa certificada en calidad del portafolio. Señal de mentalidad de proceso estructurado.
- [2026-06-17] Guastella & Asoc (Rosario, Córdoba 797 P.5): 30+ años, especializado en agro/industria/comex. Email Gmail genérico (estudiocontableguastella@gmail.com) pero SIN nombre de socio publicado. Reservar para corrida futura (investigar titular en CPCESF o LinkedIn).
- [2026-06-17] Priotti & Asociados (Rosario, con oficinas en Uruguay): email protegido por JavaScript en el sitio web. No extraíble. Estudio con perfil contable+jurídico interesante. Reservar para corrida futura (intentar vía formulario web o CPCESF).
- [2026-06-17] Rosario tiene capacidad para 10+ corridas adicionales — mercado muy poco trabajado (8 leads en total tras esta corrida, en una ciudad de 1.4M).

## Gotchas descubiertos (continuación — 2026-06-15)
- [2026-06-15] GL Estudio (Bahía Blanca): segundo email operativo estudiogl@bvconline.com.ar (BVConline, plataforma de verificación de negocios). Puede ser canal secundario si info@ no responde.
- [2026-06-15] Estudio Vermeulen (Javier Vermeulen, Neuquén + CABA, 2005): email real no extraíble del sitio (contact page 404; formato enmascarado en WebFetch). Candidato para corrida futura vía LinkedIn o CPCE Neuquén.
- [2026-06-15] RS Contadores Neuquén (Belgrano 1216): misma limitación de email enmascarado. Titular no publicado. Candidato corrida futura.
- [2026-06-15] Vaca Muerta angle: Estudio Carnicero confirma nicho de estudios contables especializados en Oil & Gas en Neuquén. Fuente valiosa: Guía Vaca Muerta (guiavacamuerta.com/categorias/estudios-contables.htm). Explorar en corrida dedicada.
- [2026-06-15] CPN Zelarayán (Neuquén): contadoras/contadores independientes sin equipo = CTA de máxima urgencia en temporada pico. Segmento a explorar más en Patagonia.
- [2026-06-15] CPCE Bahía Blanca: publica directorio de matriculados — fuente para corridas futuras en la ciudad (quedan sin cubrir Estudio Villar, Estudio Correa y otros).
- [2026-06-15] CRM stats endpoint (/api/crm/stats) respondió 401 durante la corrida. No bloquea operación pero limita la lectura de métricas de tasa de respuesta. Reportar al equipo de desarrollo.
- [2026-06-16] Hay dos estudios "Bruera" en Argentina: Estudio Bruera Santa Fe (estudiobruera.com / Mitre 5555, SF) y Estudio Bruera Córdoba (estudiobruera.com.ar / Italia 2981, Córdoba). Son estudios diferentes. No confundir al hacer outreach.
- [2026-06-16] SB Estudio Betique (SF): publica email personal slbetique@outlook.com Y sbetique@gmail.com + WhatsApp. Alta accesibilidad digital, ideal para test de primer lote cuando se active envío.
- [2026-06-16] Estudio Dutto (SF): único estudio del programa que declara servicios "informático-tecnológico". Ángulo diferenciado vs. corridas previas. Director Martín Dutto: perfil académico UNL (adoptante temprano).
- [2026-06-16] Estudio Capri (SF): email alternativo recepcion@estudiocapri.com y aangeloni@estudiocapri.com (San Justo). Usar si mcapri@ no responde.
- [2026-06-16] Sitios caídos en Paraná esta corrida: escales.com.ar (503), durandoyasociados.com.ar (ECONNREFUSED), estudiodlc.com (ECONNREFUSED), diaz-barzola.com.ar (403). Socios DLC identificados: Deharbe, Castellani, López. Todos son candidatos para corrida futura.
- [2026-06-16] paranaonline.com.ar lista estudios y contadores en Paraná con datos. Fuente valiosa para corridas futuras en Entre Ríos (Paraná, Concordia, Gualeguaychú, Colón).

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
- Corridas borrador completadas: 11/06 (Córdoba/Rosario), 12/06 (CABA/GBA), 13/06 (Mendoza/Tucumán), 14/06 (Salta/Mar del Plata), 15/06 (Bahía Blanca/Neuquén), 16/06 (Santa Fe/Paraná), 17/06 (Rosario expansión), 18/06 (San Juan/Resistencia Chaco), 19/06 (Jujuy/Posadas Misiones), 20/06 (La Rioja Capital/Catamarca Capital) → **50 leads en borrador (10 corridas)**. Cinturón NOA completo (Mendoza, Tucumán, Salta, Jujuy, La Rioja, Catamarca).
- Pendiente real: validar calidad de los emails y, cuando se apruebe, encender el envío (flip a push-vivo).

## Última corrida
**Fecha:** 2026-06-20 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **La Rioja Capital** (primera incursión) + **San Fernando del Valle de Catamarca** (primera incursión)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 2 (Marnetto: dominio propio ✅, M&S: Gmail)
**Sin email:** 3 (Rivera Michea, Melnik ⭐⭐, Boggio)
**Email status:** 1 verificado dominio propio (Marnetto ⭐), 1 Gmail (M&S), 3 not_found
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026)
**Archivos:**
- `funnel/leads/new/borrador-2026-06-20.jsonl` — 5 leads
- `funnel/reportes/2026-06-20.md` — reporte completo
**Total acumulado borrador:** 50 leads (10 corridas)
**Próximo bloqueante:** Validar calidad de emails y activar envío real (`OUTREACH_ENABLED=true` + warm-up). Prioridad: emails personales verificados — Bisonni ⭐⭐, Herusa, Pereiro (06-17), Betique (06-16), Torre-Pulisich (06-13), Farina (06-13), Posadas (06-14). Nuevos candidatos NOA: Rojas Naser ⭐⭐ (tech-adjacent Jujuy), Lasquera ⭐, Alvarenga ⭐ (primer Misiones), Marnetto ⭐ (La Rioja). Candidato PRIORITARIO sin email: Melnik ⭐⭐ (Catamarca — docente digitalización CPCE, mismo perfil que Rojas Naser).

## Corrida anterior (2026-06-19)
**Fecha:** 2026-06-19 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **San Salvador de Jujuy** (NOA — primera incursión en la provincia) + **Posadas, Misiones** (NEA — primera incursión en Misiones)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 5 (todos con email y copy completo)
**Email status:** 3 verificados de dominio propio (Lasquera, Rojas Naser ⭐⭐, Alvarenga ⭐), 1 Gmail (Zampini), 1 inferido (Grosso Juárez — arnet.com.ar, validar antes de envío)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026)
**Archivos:**
- `funnel/leads/new/borrador-2026-06-19.jsonl` — 5 leads
- `funnel/reportes/2026-06-19.md` — reporte completo
**Total acumulado borrador:** 45 leads (9 corridas)

## Corrida anterior (2026-06-18)
**Fecha:** 2026-06-18 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **San Juan Capital** (Cuyo) + **Resistencia, Chaco** (NEA — primera incursión)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 5 (todos con email y copy completo)
**Email status:** 5 emails de dominio/estudio (0 personales esta corrida); Pronea ⭐ y San Cristóbal ⭐ como candidatos para primer envío en el NEA
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026)
**Archivos:**
- `funnel/leads/new/borrador-2026-06-18.jsonl` — 5 leads
- `funnel/reportes/2026-06-18.md` — reporte completo
**Total acumulado borrador:** 40 leads (8 corridas)

## Corrida anterior (2026-06-17)
**Fecha:** 2026-06-17 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Rosario expansión** (Gran Rosario)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 5 (todos con email y copy completo)
**Email status:** 3 personales verificados (Bisonni: daniel.bisonni@hotmail.com.ar ⭐⭐, Herusa: cpnsamuel@outlook.com ⭐, Pereiro: gustavopereiro@hotmail.com ⭐), 2 genéricos de dominio
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026)
**Archivos:**
- `funnel/leads/new/borrador-2026-06-17.jsonl` — 5 leads
- `funnel/reportes/2026-06-17.md` — reporte completo
**Total acumulado borrador:** 35 leads (7 corridas)

## Corrida anterior (2026-06-16)
**Fecha:** 2026-06-16 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — Santa Fe Capital + Paraná (Entre Ríos) — Corredor Litoral
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 5 (todos con email y copy completo)
**Email status:** 1 personal verificado (Betique: slbetique@outlook.com ⭐), 4 genéricos/de estudio
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026)
**Archivos:**
- `funnel/leads/new/borrador-2026-06-16.jsonl` — 5 leads
- `funnel/reportes/2026-06-16.md` — reporte completo
**Total acumulado borrador:** 30 leads (6 corridas)

## Corrida anterior (2026-06-15)
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
- [2026-06-17] Corrida de expansión profunda en Rosario (3ª ciudad del país, sub-prospectada). 3 emails personales verificados (Bisonni, Herusa, Pereiro) — mejor tasa de emails personales de todo el programa hasta ahora. Nuevos ángulos: BI/tableros (Bisonni), recupero IVA comex (Pereiro), ISO 9001 (Contadores Rosario). CRM 5/5 × 200.
- [2026-06-16] Corrida expandida al Corredor Litoral: Santa Fe Capital + Paraná (Entre Ríos). Primer lead de Paraná (Borré & Asociados). Nuevo ángulo tech-adjacent para Dutto (único estudio que declara servicios informáticos). 5 emails escritos, 1 email personal verificado (Betique). CRM 5/5 × 200.
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
