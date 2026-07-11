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

## Gotchas descubiertos (continuación — 2026-07-10)
- [2026-07-10] Estudio Mancinella & Asociados (Moreno, ~20 años): Pablo Mancinella, fundador. Email info@estudiomancinella.com.ar (dominio propio, verificado). Servicios: auditoría, RRHH/sueldos, impuestos AFIP/ARBA, consultoría administrativa. Perfil PyME consolidado en GBA Oeste. Candidato ⭐ primer envío en Moreno. Ángulo: casi 20 años de trayectoria = cartera pesada, automatizar el flujo manual es el siguiente paso obvio.
- [2026-07-10] Sendros & Asociados (Moreno, desde 2013): CP Tatiana Sendros, fundadora. España 714 4to A, Moreno. Email info@estudiosendros.com.ar (dominio propio, verificado). Especialidad: PyMEs y cooperativas = vencimientos cruzados en julio. Candidata ⭐ primer envío en Moreno.
- [2026-07-10] SMA Estudio Contable Integral (Moreno): titular S. Arias (nombre completo no publicado). Victorica 525, Moreno. Email nominativo sarias@smaestudio.com.ar (dominio propio, verificado). Servicios integrales: impuestos, sueldos, balances, auditorías, trámites IGJ/DPPJ. Email nominativo con inicial solamente — personalización reducida.
- [2026-07-10] Estudio Contable Blanco (Moreno, 35+ años): sin email publicado. Sitio web estudioblanco.net con error 503. Presencia en redes (@estudiocontableblanco, blancoestudiocontable). Candidato para corrida futura cuando el sitio esté operativo o vía CPBA delegación Moreno.
- [2026-07-10] **Moreno (GBA Oeste):** municipio de ~450k hab. Densidad media de estudios con web propia. cercanooeste.com es la fuente más efectiva para la zona. Capacidad 5+ corridas adicionales. Candidatos pendientes: Estudio Blanco (buscar email), Estudio Contable Impositivo Moreno, Estudio Jurídico Contable MG, otros en licuo.com.ar/moreno y cercanooeste.com.
- [2026-07-10] **José C. Paz (GBA Norte):** municipio de ~300k hab. BAJA presencia digital de estudios contables — ninguno con web propia encontrada, solo Facebook/Instagram. Estrategia recomendada: CPBA delegación José C. Paz para obtener directorio de matriculados con emails. Arriegui es el único lead con identidad mínima (Facebook) en esta corrida. Mercado existe pero requiere estrategia alternativa.
- [2026-07-10] **HITO: 150 leads en borrador (30 corridas).** Moreno (GBA Oeste) inaugurado ✓. José C. Paz (GBA Norte) inaugurado ✓. GBA: 17 municipios cubiertos. Hito de 150 leads.
- [2026-07-10] **ALERTA TIMING MÁXIMA (17 días):** el vencimiento RG ARCA 5851/2026 (27/07/2026) está a 17 días. Con 150 leads en Contactos (≥130 con email válido), urgencia máxima para activar `OUTREACH_ENABLED=true`.

## Gotchas descubiertos (continuación — 2026-07-07)
- [2026-07-07] Estudio Paz & Asoc. (Vicente López, 2022): Pablo Alejandro Paz, fundador. Ávalos 2829, VL. Email info@estudiopaz.com.ar (dominio propio, verificado). Blog técnico activo con artículos recientes sobre ARBA/AGIP. Perfil de adoptador temprano ⭐. Ángulo: estudio joven y digital — OPTIMIZAR es la capa de automatización que le sigue al crecimiento digital.
- [2026-07-07] Parra Estudio Contable (Olivos, Vicente López, 25+ años): sin nombre de socio publicado. Email consultas@estudioparra.com.ar (dominio propio, verificado). Carlos Gardel 2001, Olivos. Sitio: estudio-parra.com. Cartera consolidada en zona de alta renta. Candidato para corrida futura con investigación adicional del nombre del socio vía CPBA delegación Vicente López.
- [2026-07-07] Estudio Contable Collado (Vicente López, 30+ años): email estudiocollado@gmail.com obtenido del registro oficial de comercios del municipio (comercios.vicentelopez.gov.ar). Ing. Guillermo Marconi 2324. Tel.: 11 6525-2656. Nombre de socio no publicado. 30+ años + cartera PyME = alto volumen DDJJ julio. Candidato para buscar nombre socio vía CPBA.
- [2026-07-07] Estudio Contable MD (Tigre, fundado por D'Agostino + Mammarella): PRIMER ESTUDIO 100% DIGITAL del programa. Sin sede física, operación virtual completa. CP Juan Ignacio D'Agostino (UBA) + CP Lucila Belén Mammarella (UNSAM). Email nominativo ignacio.dagostino@mdestudiocontable.com.ar. Matriculado CPCE PBA + CPCECABA. Ángulo diferenciado único: "ya eliminaron la oficina, automatizar el flujo manual es el paso siguiente obvio". Candidato ⭐ primer envío en Tigre.
- [2026-07-07] Estudio Trinchinetti (San Fernando, matrimonio CPNs): Dr. Carlos A. Trinchinetti + Dra. Adriana E. Trinchinetti. Junín 1356, San Fernando. Email clientes@estudiotrinchinetti.com.ar (dominio propio). Servicios societarios + fiscales + administraciones rurales = vencimientos cruzados múltiples en julio. Candidato ⭐ primer envío en San Fernando.
- [2026-07-07] **Vicente López:** municipio de alta renta del GBA Norte (~270k hab). Directorio oficial de comercios (comercios.vicentelopez.gov.ar) es fuente confiable con email y teléfono verificados por el municipio. Alta densidad de estudios con web propia. Capacidad 10+ corridas. Candidatos pendientes: Budic Antonio (J. de Garay 2509, Olivos — sin email, investigar CPBA), P&L Estudio (sitio caído HTTP 500), Estudio Integral TAS (@estudiointegraltas Instagram).
- [2026-07-07] **Tigre:** municipio en crecimiento del GBA Norte (~350k hab). Primer estudio digital nativo (MD) encontrado. Baja saturación de propuestas tech. Candidatos pendientes para corridas futuras: otros estudios en licuo.com.ar/tigre, Don Torcuato, General Pacheco. Capacidad 5+ corridas.
- [2026-07-07] **San Fernando:** primer estudio encontrado con perfil rural+societario (Trinchinetti). Mercado con potencial. Capacidad 5+ corridas.
- [2026-07-07] **HITO: 135 leads en borrador (27 corridas).** Vicente López (GBA Norte) inaugurada ✓. Tigre (GBA Norte) inaugurado ✓. San Fernando (GBA Norte) inaugurado ✓. GBA: 11 municipios cubiertos. Próximos GBA sugeridos: San Isidro, Hurlingham, Pilar, Florida orbital.
- [2026-07-07] **ALERTA TIMING MÁXIMA (20 días):** el vencimiento RG ARCA 5851/2026 (27/07/2026) está a 20 días. Con 135 leads en Contactos (≥115 con email válido), el warm-up debe iniciarse urgente. La ventana de activación óptima SE CERRÓ — cada día adicional sin envío reduce la efectividad del timing.

## Gotchas descubiertos (continuación — 2026-06-30)
- [2026-06-30] Pagliano Ciencias Económicas (San Rafael, Mendoza): Diego Hernán Pagliano, CPN + Lic. Adm. Empresas (UNCuyo), CUIT 20-25766335-4 verificado. Estudio unipersonal, mentor en Cámara de Comercio de San Rafael. Email personal Gmail verificado vía CUITonline. Primer candidato ⭐ San Rafael. Ángulo: estudio unipersonal = todo el pico de julio recae sobre él.
- [2026-06-30] Estudio Contable AG (San Rafael, Mendoza): socios Renzo O. Gili Carrillo (CPN UNCuyo) + María Celeste Andreoni. Barcala 547 Of. 2-3 / Av. Rivadavia 55, San Rafael. Email genérico info@estudiocontableag.com (dominio propio). Segundo lead San Rafael. Buscar email personal de Gili Carrillo vía CPCE Mendoza para corrida futura.
- [2026-06-30] ECOAG (Olavarría, Buenos Aires): estudio especializado en gestión agropecuaria. Titular Giacomaso (inicial S., nombre no confirmado). Email sgiacomaso@gmail.com visible en ecoag.com.ar. Cartera en 6 ciudades PBA (productores agro). Primer lead Olavarría. Ángulo: cartera agro = DDJJ complejas en julio.
- [2026-06-30] Estudio Contable Ibarlucía (Olavarría, Buenos Aires): Contadora Vanesa Ibarlucía. Av. Colón 1919, Olavarría. Email estudiocontableibarlucia@gmail.com verificado en sitio propio. Cartera diversa: cooperativas, constructoras, fideicomisos. Segundo lead Olavarría con email verificado.
- [2026-06-30] Estudio Secondi & Asociados (Olavarría, Buenos Aires): Belgrano 2013. Clientes corporativos: Arcor, Loma Negra, La Serenísima, Papel Misionero, CMPC, Cementos Avellaneda. Sistema propio e-7400. Sin email publicado ni nombre de titular. Candidato ⭐ para corrida futura — investigar vía CPBA Olavarría o LinkedIn. Perfil corporativo diferente al ICP habitual pero potencial alto.
- [2026-06-30] San Rafael, Mendoza: baja presencia digital en estudios contables. La mayoría solo figura en directorios (Licuo, MisterWhat, PaginasAmarillas) con teléfono y dirección pero sin web propia ni email. Fuente efectiva: búsquedas de nombre en Facebook + Google. CPCEMZA (cpcemza.org.ar) tiene padrón de matriculados accesible y delegación San Rafael — fuente clave para próximas corridas. Capacidad para 10+ corridas en San Rafael (23+ estudios en MisterWhat, 17+ en guia-mendoza, 18+ en infoisinfo pero sin contacto digital).
- [2026-06-30] Olavarría, Buenos Aires: primera incursión exitosa. Hub agroindustrial (~100k hab, Loma Negra/cemento + agro). Baja exposición tech = diferenciador real. Candidatos adicionales para próximas corridas: Gelso-Destassi (9 de julio 2369, tel 02284 441992), Arias & Asociados (sgto cabral 2811), Dietrich Estudio Contable (Alsina 2521), Álvarez Castarés (Facebook activo, buscar email), Nemcek Juan Pablo (negocio.site caído hoy). Fuente: olavarria.licuo.com.ar (18 resultados), olavarria.infoisinfo-ar.com.
- [2026-06-30] **HITO: 100 leads en borrador (20 corridas).** San Rafael (Mendoza) inaugurada ✓. Olavarría (Buenos Aires) inaugurada ✓. Mendoza interior abierto (San Rafael). PBA centrosur abierto (Olavarría).

## Gotchas descubiertos (continuación — 2026-06-29)
- [2026-06-29] Estudio Bocco (Villa María, Córdoba, 13 años, agropecuario): dominio propio verificado (info@estudiobocco.com). Matrícula 10-17852-6. Especializado en tributación + agro + laboral. Candidato ⭐ para primer envío en Villa María. Ángulo: zona agropecuaria con clientes BP y Ganancias = julio es el mes más intenso del año.
- [2026-06-29] Estudio Barceló (Villa María): email personal Yahoo publicado en sitio propio (ebarcelogili@yahoo.com.ar). CPN María José Barceló. Contacto fácil, estudio orientado a PyMEs y particulares.
- [2026-06-29] Alvarez & Asociados S.A.S. (Villa María, ~40 años, fundado 1986, CUIT 30-71631053-8): sin email ni nombre de titular publicado. Sitio caído (503). Investigar vía CPCE Córdoba delegación Villa María (Mendoza 1439, Villa María). Candidato ⭐ para corrida futura.
- [2026-06-29] Estudio Ronconi (Gualeguaychú, Entre Ríos): CPN Alejandra M. Ronconi (matrícula 3019), estudio unipersonal. Email Gmail verificado en sitio Wix. Ángulo: la carga operativa de un estudio unipersonal en julio es la más alta del año.
- [2026-06-29] Estudio Fernandez Tesone (Gualeguaychú, +40 años, +200 empresas activas ⭐): el prospecto de mayor volumen de esta corrida. Sin email ni titular publicado. Sitio caído. Candidato prioritario para corrida futura vía CPCE Entre Ríos delegación Gualeguaychú. Con 200+ empresas en cartera, es el prospecto de mayor impacto potencial de todo Gualeguaychú.
- [2026-06-29] Villa María tiene capacidad para 5+ corridas adicionales. Candidatos pendientes: Magnago (mencionado corrida 06-25, email pendiente CPCE Córdoba), otros estudios en buscador5900.com.ar/profesionales, CPCE Córdoba delegación Villa María como fuente.
- [2026-06-29] Gualeguaychú: primera incursión exitosa. Hub turístico-industrial ~90k hab. Baja exposición tech = diferenciador real. Candidatos adicionales: Estudio Grosso (telexplorer.com.ar/Gualeguaychu), Estudio Vásquez, Estudio Pagnanini. CPCE Entre Ríos delegación Gualeguaychú como fuente para próximas corridas.
- [2026-06-29] Entre Ríos completa: Paraná ✓, Concordia ✓, Gualeguaychú ✓. Córdoba interior: Río Cuarto ✓, Villa María ✓. Hito 95 leads (19 corridas).

## Gotchas descubiertos (continuación — 2026-06-28)
- [2026-06-28] SAIPE Estudio Contable S.A. (Rafaela, SF): firma S.A. multi-sucursal con 6 sedes (Rafaela, Humberto, Ataliva, Sarmiento, Vera, Reconquista). 4 socios con emails personales en dominio propio: alfiore@saipe.com.ar (fundador), mbruno@saipe.com.ar (impuestos), fabioairasca@ y mgrande@ (inferidos). Candidato ⭐ para primer envío en Rafaela. Ángulo multi-sucursal: cada hora automatizada se multiplica por 6 sedes.
- [2026-06-28] Laura, Sasia y Asociados S.A. (Rafaela, SF, 70 años): la firma más antigua de la corrida y del programa. José Sasia verificado en LinkedIn. Email info@ls-sa.com.ar. Ángulo diferenciado: "70 años de adaptación constante = la firma que siempre adoptó lo que venía". Candidato ⭐ para primer envío en Rafaela.
- [2026-06-28] Estudio Ayuste (Rafaela, SF, 30+ años): equipo de 5+ profesionales con emails en dominio propio (cayuste@, lpietrobon@, mrbarberis@, fgaggiotti@, sbersano@). Email personal de titular verificado. Candidato sólido para primer envío.
- [2026-06-28] Rafaela, Santa Fe: ciudad con alta densidad de estudios con web propia y emails publicados. Capacidad para 5+ corridas adicionales. Candidatos pendientes: Cassina (Alvear 360, sin email), Ingaramo (Colón 332, sin email), Carlos Sara y Asoc (San Martín 226, sin email). Fuentes: rafaela.licuo.com.ar, argentino.com.ar/rafaela, Páginas Amarillas Rafaela.
- [2026-06-28] Junín, Buenos Aires: mercado con BAJA presencia digital — ningún estudio contable tiene web indexada ni email publicado en directorios. Estrategia recomendada: contactar CPBA delegación Junín (dlgjunin@cpba.com.ar / 0236-443-3952) para obtener padrón de matriculados con emails. Firmas objetivo: Daniel Massari ⭐ (Suárez 225), Balbi-Bergamini ⭐ (A Roca 119), Di Prinzio (Lavalle 120), García (B De Miguel 111). El mercado existe (hub agroindustrial ~100k hab) pero requiere estrategia de contacto alternativa.
- [2026-06-28] Hito: 90 leads en borrador (18 corridas). Rafaela SF inaugurada ✓. Junín BA inaugurado ✓. Santa Fe interior: Rafaela ✓ (suma a: Santa Fe Capital ✓, Rosario ✓, Paraná ✓).

## Estado del sistema (infra — lo mantiene el equipo de desarrollo, NO lo cambian las corridas)
- Plataforma OPTIMIZAR **deployada en producción** (EasyPanel): CRM + Prospección IA operativos.
- Backend: endpoints externos OK, **migración aplicada**, **chat en vivo sobre el plan funcionando**.
- **Prospección diaria automática: ACTIVA en MODO BORRADOR** (busca y escribe; NO envía nada).
- **Envío real de correos: APAGADO** (`OUTREACH_ENABLED=false`). Encender tras validar emails + warm-up.
- Corridas borrador completadas: 11/06 (Córdoba/Rosario), 12/06 (CABA/GBA), 13/06 (Mendoza/Tucumán), 14/06 (Salta/Mar del Plata), 15/06 (Bahía Blanca/Neuquén), 16/06 (Santa Fe/Paraná), 17/06 (Rosario expansión), 18/06 (San Juan/Resistencia Chaco), 19/06 (Jujuy/Posadas Misiones), 20/06 (La Rioja Capital/Catamarca Capital), 21/06 (La Plata/San Luis Capital), 22/06 (Córdoba 2° lote/Comodoro Rivadavia), 23/06 (Corrientes Capital/Santiago del Estero Capital), 24/06 (Formosa Capital/Bariloche Río Negro), 25/06 (Río Cuarto/Río Gallegos Santa Cruz), 26/06 (Tandil/General Roca Río Negro), 27/06 (Concordia Entre Ríos/Pergamino Buenos Aires), 28/06 (Rafaela Santa Fe/Junín Buenos Aires), 29/06 (Villa María Córdoba/Gualeguaychú Entre Ríos), 30/06 (San Rafael Mendoza/Olavarría Buenos Aires), 01/07 (Ushuaia Tierra del Fuego/Necochea Buenos Aires), 02/07 (San Nicolás de los Arroyos Buenos Aires/Venado Tuerto Santa Fe), 03/07 (Lomas de Zamora GBA Sur/Morón GBA Oeste), 04/07 (Quilmes GBA Este/Avellaneda GBA Sur), 05/07 (Lanús GBA Sur/General San Martín GBA Norte), 06/07 (Merlo GBA Oeste/Tres de Febrero GBA Oeste), 07/07 (Vicente López GBA Norte/Tigre+San Fernando GBA Norte), 08/07 (San Isidro GBA Norte/Pilar GBA Norte), 09/07 (Hurlingham GBA Oeste/Escobar GBA Norte), 10/07 (Moreno GBA Oeste/José C. Paz GBA Norte), 11/07 (**San Miguel GBA Norte/Malvinas Argentinas GBA Norte**) → **155 leads en borrador (31 corridas)**. Cinturón NOA completo (Mendoza, Tucumán, Salta, Jujuy, La Rioja, Catamarca, Santiago del Estero ✓). Cuyo completo (Mendoza, San Juan, San Luis). Mendoza interior: San Rafael ✓. Patagonia: Neuquén ✓, Comodoro ✓, Bariloche ✓, Río Gallegos ✓, General Roca ✓, Ushuaia ✓. NEA completo: Chaco ✓, Misiones ✓, Corrientes ✓, Formosa ✓. Córdoba interior: Río Cuarto ✓, Villa María ✓. PBA interior: La Plata ✓, Bahía Blanca ✓, Mar del Plata ✓, Tandil ✓, Pergamino ✓, Junín ✓, Olavarría ✓, Necochea ✓, San Nicolás de los Arroyos ✓. Entre Ríos completo: Paraná ✓, Concordia ✓, Gualeguaychú ✓. Santa Fe interior: Rafaela ✓, Venado Tuerto ✓. GBA municipios: Lomas de Zamora ✓, Morón ✓, Quilmes ✓, Avellaneda ✓, Lanús ✓, General San Martín ✓, Merlo ✓, Tres de Febrero ✓, Vicente López ✓, Tigre ✓, San Fernando ✓, San Isidro ✓, Pilar ✓, Hurlingham ✓, Escobar ✓, Moreno ✓, José C. Paz ✓, **San Miguel ✓, Malvinas Argentinas ✓** (19 municipios GBA cubiertos).
- Pendiente real: validar calidad de los emails y, cuando se apruebe, encender el envío (flip a push-vivo).

## Gotchas descubiertos (continuación — 2026-07-11)
- [2026-07-11] Estudio Contable Paredes (San Miguel): Dr. Christian M. Paredes (CP + Lic. Administración). San Miguel, PBA. Email contacto@estudioparedes.com.ar (dominio propio, verificado). Atención integral a empresas, comercios y particulares; también atiende en CABA. Perfil dual = cartera heterogénea con múltiples tipos de declaración en julio. Candidato ⭐ primer envío en San Miguel.
- [2026-07-11] Santarsiero Videla (San Miguel, desde 2005): Romina Santarsiero + Claudio Martín Videla. Rodríguez Peña 952, San Miguel. Email info@santarsiero-videla.com.ar (dominio propio, verificado). Servicios: impuestos, sueldos, auditoría de estados contables, constitución de sociedades. 20+ años con dos socios = alto volumen de liquidaciones en julio. Candidato ⭐ primer envío en San Miguel.
- [2026-07-11] Dr. Daniel Gustavo Constantin (Bella Vista, Partido San Miguel): San Juan 1508, Bella Vista. Email info@estudiodgconstantin.com.ar (dominio propio verificado). Email alternativo: daniel@estudiodgconstantin.com.ar. Servicios: impositivo, laboral, contable y societario. Énfasis en ética y discreción. Primer estudio de Bella Vista en el programa. Candidato ⭐ primer envío en Bella Vista.
- [2026-07-11] Flores & García Asociados (Los Polvorines, Malvinas Argentinas, 16+ años): CP Santiago Flores + CP Cecilia García. Sitio propio activo (estudiofloresgarciaasoc.com.ar) que devuelve 403 para crawlers. Email no indexado en ningún directorio público. Primer estudio de Malvinas Argentinas en el programa. Acción futura: formulario web o CPBA delegación Malvinas Argentinas.
- [2026-07-11] Dra. María E. Medvedev (Los Polvorines, Malvinas Argentinas): Perfil LinkedIn activo ("Estudio Contable Malvinas Argentinas") + Facebook. También figura en directorio Bella Vista/San Miguel junto a Víctor Hugo Anzuinelli (Serrano 1645, tel. 4667-0933) — posible red de colaboración o doble sede. Email no publicado. Candidata para corrida futura vía Facebook/LinkedIn o CPBA.
- [2026-07-11] **San Miguel (Partido de San Miguel, ~280k hab):** alta densidad digital — 3/3 leads con email verified_domain en primera incursión. Bella Vista pertenece al Partido de San Miguel (CP B1661). Municipio con capacidad 10+ corridas adicionales. Candidatos pendientes: gbk Estudio Contable (Paunero 460, SM), Murphy-Bortot (Sarmiento 1496, SM), Caironi-Larrechea (Ángel D'Elía 1158, SM), Estudio RLB (Gúemes 1221, SM), Dra. Natalia Nuñez (Sarmiento 1697, SM). Fuentes: zonaclick.com.ar/rubros/estudios-contables, guiadebellavista.com.ar.
- [2026-07-11] **Malvinas Argentinas (Los Polvorines/Grand Bourg, ~320k hab):** presencia digital similar a José C. Paz — mayoría de estudios solo con teléfono en directorios. Flores & García y Medvedev son los únicos con identidad digital mínima. CPBA delegación Malvinas Argentinas es la fuente recomendada para próximas corridas. Capacidad 5+ corridas con investigación adicional.
- [2026-07-11] **HITO: 155 leads en borrador (31 corridas).** San Miguel (GBA Norte) inaugurado ✓. Malvinas Argentinas (GBA Norte) inaugurado ✓. GBA: 19 municipios cubiertos. Próximos GBA sugeridos: Florencio Varela (GBA Sur), Berazategui (GBA Este), San Miguel 2ª vuelta (gbk + Murphy-Bortot + Caironi-Larrechea).
- [2026-07-11] **ALERTA TIMING MÁXIMA (16 días):** el vencimiento RG ARCA 5851/2026 (27/07/2026) está a 16 días. Con 155 leads en Contactos (≥135 con email válido), urgencia máxima para activar `OUTREACH_ENABLED=true`.

## Última corrida
**Fecha:** 2026-07-11 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **San Miguel (GBA Norte)** (primera incursión — ~280k hab, Partido de San Miguel) + **Malvinas Argentinas (GBA Norte)** (primera incursión — ~320k hab, Los Polvorines)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; sin duplicados)
**Emails escritos:** 3 (Paredes ✅ dominio propio, Santarsiero Videla ✅ dominio propio, Constantin ✅ dominio propio)
**Sin email:** 2 (Flores & García — sitio 403; Medvedev — sin email indexado)
**Email status:** 3 verified_domain (Paredes contacto@estudioparedes.com.ar, Santarsiero Videla info@santarsiero-videla.com.ar, Constantin info@estudiodgconstantin.com.ar), 2 not_found (Flores & García, Medvedev)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan **16 días**.
**Archivos:**
- `funnel/leads/new/borrador-2026-07-11.jsonl` — 5 leads
- `funnel/reportes/2026-07-11.md` — reporte completo
**Total acumulado borrador:** 155 leads (31 corridas)
**Hitos:** San Miguel (GBA Norte) inaugurado ✓. Malvinas Argentinas (GBA Norte) inaugurado ✓. GBA: 19 municipios cubiertos. Candidatos ⭐ nuevos: Santarsiero Videla (20 años, dos socios, auditoría), Paredes (doble titulación, cartera mixta), Constantin (impositivo + societario, Bella Vista). Candidatos pendientes San Miguel: gbk, Murphy-Bortot, Caironi-Larrechea, RLB, Nuñez. Candidatos pendientes Malvinas Argentinas: buscar email Flores & García vía formulario o CPBA.
**Próximo bloqueante:** Validar calidad de los emails y activar envío real (`OUTREACH_ENABLED=true` + warm-up). **ALERTA TIMING CRÍTICA:** quedan 16 días para el 27/07/2026. Con 155 leads en Contactos (≥135 con email válido), cada día sin envío reduce la efectividad del disparador.

## Corrida anterior (2026-07-10)
**Fecha:** 2026-07-10 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Moreno (GBA Oeste)** (primera incursión — municipio GBA Oeste, ~450k hab) + **José C. Paz (GBA Norte)** (primera incursión — corredor norte, ~300k hab)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 3 (Mancinella ✅ dominio propio, Sendros ✅ dominio propio, SMA/Arias ✅ nominativo dominio propio)
**Sin email:** 2 (Blanco — sitio 503; Arriegui JC Paz — solo Facebook)
**Email status:** 3 verified_domain (Mancinella info@estudiomancinella.com.ar, Sendros info@estudiosendros.com.ar, SMA sarias@smaestudio.com.ar), 2 not_found (Blanco, Arriegui)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan **17 días**.
**Archivos:**
- `funnel/leads/new/borrador-2026-07-10.jsonl` — 5 leads
- `funnel/reportes/2026-07-10.md` — reporte completo
**Total acumulado borrador:** 150 leads (30 corridas)
**Hitos:** Moreno (GBA Oeste) inaugurado ✓. José C. Paz (GBA Norte) inaugurado ✓. GBA: 17 municipios cubiertos. **HITO: 150 leads en borrador (30 corridas)**. Candidatos pendientes Moreno: cercanooeste.com tiene más estudios, Estudio Blanco (35+ años, buscar email corrida futura). Candidatos pendientes José C. Paz: baja presencia digital, fuente recomendada CPBA delegación JC Paz. Próximos GBA sugeridos: Escobar 2ª vuelta (DAZ + Dr. Rojas + Lamota), San Isidro 2ª vuelta (SGB Contadores + Aguilar), Malvinas Argentinas, San Miguel.
**Próximo bloqueante:** Validar calidad de los emails y activar envío real (`OUTREACH_ENABLED=true` + warm-up). **ALERTA TIMING CRÍTICA:** quedan 17 días para el 27/07/2026. Con 150 leads en Contactos (≥130 con email válido), cada día sin envío reduce la efectividad del disparador.

## Corrida anterior (2026-07-09)
**Fecha:** 2026-07-09 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Hurlingham (GBA Oeste)** (primera incursión — municipio GBA Oeste, ~180k hab) + **Belén de Escobar (GBA Norte)** (primera incursión — corredor norte, ~250k hab)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 4 (Toloza ✅ personal, SNS ✅ dominio propio, Valerga ✅ personal, Bissio ✅ dominio propio)
**Sin email:** 1 (Monica Martinez — solo teléfono)
**Email status:** 2 verified_personal (Toloza tolozar@hotmail.com, Valerga leovalerga@gmail.com), 2 verified_domain (SNS contacto@estudiosns.com.ar, Bissio info@estudiobissio.com.ar), 1 not_found (Martinez)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan **18 días**.
**Archivos:**
- `funnel/leads/new/borrador-2026-07-09.jsonl` — 5 leads
- `funnel/reportes/2026-07-09.md` — reporte completo
**Total acumulado borrador:** 145 leads (29 corridas)
**Hitos:** Hurlingham (GBA Oeste) inaugurado ✓. Escobar/Belén de Escobar (GBA Norte) inaugurado ✓. GBA: 15 municipios cubiertos. Candidato ⭐ nuevo: Bissio & Asociados (30+ años, 3 socios familia, atención personal directa).

## Corrida anterior (2026-07-08)
**Fecha:** 2026-07-08 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **San Isidro (GBA Norte)** (primera incursión — municipio de mayor renta GBA Norte, ~350k hab) + **Pilar (GBA Norte, corredor Panamericana)** (primera incursión — hub PyMEs norte, ~270k+ hab)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 5 (todos con email y copy completo)
**Sin email:** 0
**Email status:** 5/5 verified_domain (Ghirardotti info@ggasoc.com, Madero info@estudiomadero.com, Roldán estudio@estudioroldan.net, Mastrocola info@mastrocola.com.ar, Raposo da Silva consultas@estudiordas.com.ar) — mejor corrida de calidad email: 100% dominio propio.
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan **19 días**.
**Archivos:**
- `funnel/leads/new/borrador-2026-07-08.jsonl` — 5 leads
- `funnel/reportes/2026-07-08.md` — reporte completo
**Total acumulado borrador:** 140 leads (28 corridas)
**Hitos:** San Isidro (GBA Norte) inaugurado ✓ — municipio de mayor renta del GBA Norte. Pilar (GBA Norte) inaugurado ✓ — corredor Panamericana. GBA: 13 municipios cubiertos. Candidatos ⭐ nuevos: Ghirardotti & Ghirardotti (60 años, 500+ clientes, red BOKS International ⭐⭐), Mastrocola (50+ profesionales, mayor estudio de Pilar ⭐). Próximos GBA sugeridos: Hurlingham (Oeste), Escobar (Norte), José C. Paz (Norte), San Isidro 2ª vuelta (SGB Contadores + Aguilar & Asoc).
**Próximo bloqueante:** Validar calidad de los emails y activar envío real (`OUTREACH_ENABLED=true` + warm-up). **ALERTA TIMING CRÍTICA:** quedan 19 días para el 27/07/2026. Con 140 leads en Contactos (≥120 con email válido), cada día sin envío reduce la efectividad del disparador.

## Gotchas descubiertos (continuación — 2026-07-09)
- [2026-07-09] Suarez Nelson Sulle & Asoc (Hurlingham, 30 años): Nelson Sulle. Delfor Díaz 1651, Hurlingham. Email contacto@estudiosns.com.ar (dominio propio, verificado en página de contacto estudiosns.com.ar). Servicios: impositivo, contable, laboral, IGJ. Cartera PyMEs + autónomos = carga máxima en julio. Candidato ⭐ primer envío en Hurlingham.
- [2026-07-09] Estudio Contable Valerga (Hurlingham, CP UBA unipersonal): Leonardo Valerga. Isabel la Católica 736, Hurlingham. Email leovalerga@gmail.com (personal, indexado en Cylex). Especialidad: impositivo, monotributo, personas físicas. Estudio unipersonal = toda la carga de julio recae sobre él. Tel: 011 5133-3010.
- [2026-07-09] Estudio Bissio & Asociados S.H. (Belén de Escobar, desde 1/3/1994): Jorge Bissio (Propietario) + Darío Bissio + Luis Bissio. Dr. Travi 230, Belén de Escobar. Email info@estudiobissio.com.ar (dominio propio, verificado). Servicios: auditoría, payroll, fiscal/impuestos, asistencia en sistemas informáticos. 30+ años con modelo de atención personal directa de socios. Candidato ⭐ primer envío en Escobar.
- [2026-07-09] **Hurlingham (GBA Oeste):** municipio compacto (~180k hab). Baja presencia digital de estudios (mayoría solo tienen teléfono). Excepciones con email/web: Toloza, SNS, Valerga. Fuentes efectivas: licuo.com.ar/hurlingham + Cylex (da email en snippets de Google aunque 403 directo). Capacidad 5+ corridas adicionales. Candidatos pendientes: Monica Martinez (buscar email CPBA), Beneguen (tel solo), Tinik (tel solo), Pantanetti (tel solo), MCR (@estudio.mcr Instagram).
- [2026-07-09] **Escobar/Belén de Escobar (GBA Norte):** municipio con presencia digital variable. Candidatos ⭐ pendientes: DAZ (info@estudiodaz.com.ar, sin titular), Dr. Alberto Rojas (Ing. Maschwitz, email inferred, web 503 hoy), Lamota (solo WhatsApp, alta calidad de sitio). Fuente valiosa: puntoclick.com.ar/empresa/[nombre] — 21 fichas individuales en Belén de Escobar. Capacidad 10+ corridas.
- [2026-07-09] **HITO: 145 leads en borrador (29 corridas).** Hurlingham (GBA Oeste) inaugurado ✓. Escobar (GBA Norte) inaugurado ✓. GBA: 15 municipios cubiertos.
- [2026-07-09] **ALERTA TIMING MÁXIMA (18 días):** el vencimiento RG ARCA 5851/2026 (27/07/2026) está a 18 días. Con 145 leads en Contactos (≥125 con email válido), urgencia máxima para activar `OUTREACH_ENABLED=true`.

## Gotchas descubiertos (continuación — 2026-07-08)
- [2026-07-08] Ghirardotti & Ghirardotti S.C. (San Isidro, desde 1967): el lead más consolidado encontrado en San Isidro. Mariano Ghirardotti (Socio Director). 500+ clientes activos en agro, tecnología, construcción, minería y energía. Miembro BOKS International (red global de firmas contables). Email info@ggasoc.com (dominio propio verificado). Primer estudio de San Isidro en el programa. Ángulo: escala multiplica ROI de automatización. Candidato ⭐⭐.
- [2026-07-08] Estudio Madero & Asociados (San Isidro, 30+ años): Ignacio A. Madero, Director. 25 de Mayo 574 Piso 2 Of. 12. Sectores: agro, real estate, industria, tecnología. Email info@estudiomadero.com (verificado). Cartera multi-sector = liquidaciones complejas en julio. Candidato ⭐.
- [2026-07-08] SGB Contadores (San Isidro, 15 años): Santiago Hernán González Bonorino (fundador, UCA + posgrado EAE Barcelona, docente UDESA). Email administracion@sgbcontadores.com.ar (dominio propio) o administracionsgb@sgbcontadores.com.ar. Segunda sede en CABA (Montevideo 1012). Perfil boutique sofisticado. Candidato ⭐ para corrida futura en San Isidro.
- [2026-07-08] Mastrocola Contadores Públicos (Pilar, desde 1994): 50+ profesionales — el mayor estudio del corredor Pilar. Andrés A. Mastrocola (fundador). Email info@mastrocola.com.ar (verificado). Outsourcing contable-impositivo-administrativo como servicio central. Escala = máximo impacto de automatización. Candidato ⭐.
- [2026-07-08] Estudio Roldán (Pilar, desde 1996): Dr. Walter Omar Roldán CPN, CPCEPBA Legajo 24194/6. Email estudio@estudioroldan.net (dominio propio nominativo, acceso directo al titular). Pericias judiciales + auditoría + unipersonal = máxima carga en julio. Candidato ⭐.
- [2026-07-08] Estudio Raposo da Silva (Pilar, Paseo Vía Pilar): Cdra. Laura Raposo da Silva, contadora independiente. Email consultas@estudiordas.com.ar. Ubicación premium (centro comercial de alta visibilidad en corredor Panamericana). Experiencia corporativa (Saputo) = comprende ROI de sistemas.
- [2026-07-08] **San Isidro:** municipio de alta renta del GBA Norte (~350k hab). Alta densidad de estudios con web propia y email publicado. Corrida 5/5 verified_domain. Candidatos pendientes: SGB Contadores (⭐, González Bonorino, email verificado), Aguilar & Asociados (estudiocontableaguilar.com.ar, verificar email), otros en licuo.com.ar/san-isidro, PuntoClick, Páginas Amarillas. Capacidad 10+ corridas.
- [2026-07-08] **Pilar:** hub PyMEs del norte GBA (~270k+ hab). Mastrocola es el mayor estudio del corredor. Candidatos adicionales: Robles & Asociados (403 hoy), Organización Pilar (503 hoy), otros en argentino.com.ar/pilar y guiaurbana.com.ar. Fuente efectiva: CPBA delegación Pilar. Capacidad 10+ corridas.
- [2026-07-08] **HITO: 140 leads en borrador (28 corridas).** San Isidro (GBA Norte) inaugurado ✓. Pilar (GBA Norte) inaugurado ✓. GBA: 13 municipios cubiertos. Corrida de mejor calidad email histórica: 5/5 verified_domain.
- [2026-07-08] **ALERTA TIMING MÁXIMA (19 días):** el vencimiento RG ARCA 5851/2026 (27/07/2026) está a 19 días. Urgencia máxima para activar `OUTREACH_ENABLED=true`. Candidatos ⭐⭐ prioritarios para primer lote: Ghirardotti (San Isidro, 500+ clientes, BOKS International), MD (Tigre, digital nativo), Paz (Vicente López, blog activo), Mastrocola (Pilar, 50+ profesionales).

## Corrida anterior (2026-07-07)
**Fecha:** 2026-07-07 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Vicente López (GBA Norte)** (primera incursión — municipio de alta renta, ~270k hab) + **Tigre + San Fernando (GBA Norte)** (primera incursión — corredor norte, ~500k hab)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 5 (todos con email y copy completo)
**Sin email:** 0
**Email status:** 4 verified_domain (Paz info@, Parra consultas@, MD nominativo ignacio.@, Trinchinetti clientes@), 1 verified_personal Gmail (Collado — Gmail oficial padrón municipal Vicente López)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan **20 días**.
**Archivos:**
- `funnel/leads/new/borrador-2026-07-07.jsonl` — 5 leads
- `funnel/reportes/2026-07-07.md` — reporte completo
**Total acumulado borrador:** 135 leads (27 corridas)
**Hitos:** Vicente López (GBA Norte) inaugurada ✓. Tigre (GBA Norte) inaugurada ✓. San Fernando (GBA Norte) inaugurado ✓. GBA desagregado: 11 municipios cubiertos.

## Corrida anterior (2026-07-06)
**Fecha:** 2026-07-06 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Merlo (GBA Oeste)** (primera incursión — hub comercial/industrial GBA Oeste, ~500k hab) + **Tres de Febrero / Caseros (GBA Oeste)** (primera incursión — hub comercial GBA Oeste, ~340k hab)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 5 (todos con email y copy completo)
**Sin email:** 0
**Email status:** 3 verified_domain (Corvalán info@, Bonavota contacto@, Buffoni recepcion@), 2 verified_personal Gmail (Sirota estudiocontablesirota@gmail, Villa/Giménez estudiovillagimenez@gmail)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan 21 días.
**Archivos:**
- `funnel/leads/new/borrador-2026-07-06.jsonl` — 5 leads
- `funnel/reportes/2026-07-06.md` — reporte completo
**Total acumulado borrador:** 130 leads (26 corridas)
**Hitos:** Merlo (GBA Oeste) inaugurada ✓. Tres de Febrero/Caseros (GBA Oeste) inaugurada ✓. GBA desagregado: 10 municipios cubiertos.

## Corrida anterior (2026-07-05)
**Fecha:** 2026-07-05 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Lanús (GBA Sur)** (primera incursión — hub industrial/comercial GBA Sur, ~460k hab) + **General San Martín (GBA Norte)** (primera incursión — hub comercial/industrial GBA Norte, ~400k hab)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 4 (Scholiadis ✅ Yahoo personal, BMS ✅ dominio propio, Grasso & Challier ✅ dominio propio ⭐, EP San Martín ✅ dominio propio)
**Sin email:** 1 (Yusso — not_found, sitio HTTP 503)
**Email status:** 1 verified_personal (Scholiadis Yahoo), 3 verified_domain (BMS consultas@, Grasso info@, EP San Martín contables@), 1 not_found (Yusso)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan 22 días.
**Archivos:**
- `funnel/leads/new/borrador-2026-07-05.jsonl` — 5 leads
- `funnel/reportes/2026-07-05.md` — reporte completo
**Total acumulado borrador:** 125 leads (25 corridas)
**Hitos:** Lanús (GBA Sur) inaugurada ✓. General San Martín (GBA Norte) inaugurada ✓. GBA desagregado: CABA ✓, La Plata ✓, Lomas de Zamora ✓, Morón ✓, Quilmes ✓, Avellaneda ✓, Lanús ✓, General San Martín ✓.

## Corrida anterior (2026-07-04)
**Fecha:** 2026-07-04 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Quilmes (GBA Este)** (primera incursión — hub comercial/industrial GBA Este, ~600k hab) + **Avellaneda (GBA Sur)** (primera incursión — hub metalúrgico/industrial, limita con CABA)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 5 (todos con email y copy completo)
**Sin email:** 0
**Email status:** 4 verified_domain (GQM contacto@, D'Ambrosio info@, Gestión Sur info@, Fulleri jfulleri@), 1 verified_personal (Vitacca ivitacca@yahoo)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan 23 días.
**Archivos:**
- `funnel/leads/new/borrador-2026-07-04.jsonl` — 5 leads
- `funnel/reportes/2026-07-04.md` — reporte completo
**Total acumulado borrador:** 120 leads (24 corridas)
**Hitos:** Quilmes (GBA Este) inaugurada ✓. Avellaneda (GBA Sur) inaugurada ✓. GBA continúa desagregándose por municipio. 120 leads acumulados.

## Corrida anterior (2026-07-03)
**Fecha:** 2026-07-03 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Lomas de Zamora (GBA Sur)** (primera incursión — hub comercial/industrial GBA Sur, ~800k hab) + **Morón (GBA Oeste)** (primera incursión — hub comercial GBA Oeste, ~350k hab)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 5 (todos con email y copy completo)
**Sin email:** 0
**Email status:** 3 verified_domain (Mascheroni info@, Domínguez adm@, Morgado info@), 1 verified_personal (Gattel Gmail sitio), 1 inferred_domain (Robledo contacto@ — sitio 503, email desde snippet Google)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan 24 días.
**Archivos:**
- `funnel/leads/new/borrador-2026-07-03.jsonl` — 5 leads
- `funnel/reportes/2026-07-03.md` — reporte completo
**Total acumulado borrador:** 115 leads (23 corridas)
**Hitos:** Lomas de Zamora (GBA Sur) inaugurada ✓. Morón (GBA Oeste) inaugurada ✓. GBA comienza a desagregarse por municipio. 115 leads acumulados.

## Corrida anterior (2026-07-02)
**Fecha:** 2026-07-02 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **San Nicolás de los Arroyos (Buenos Aires)** (primera incursión — PBA norte industrial) + **Venado Tuerto (Santa Fe)** (primera incursión — hub sojero SF interior)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 2 (Gómez & Faldani ✅ dominio propio, Poszler ✅ Gmail personal ⭐⭐)
**Sin email:** 3 (Bettiolo-Parodi-Lázaro, Riccardini, Peláez — not_found)
**Email status:** 1 verified_domain (Gómez & Faldani info@), 1 verified_personal (Poszler Gmail), 3 not_found
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan 25 días.
**Archivos:**
- `funnel/leads/new/borrador-2026-07-02.jsonl` — 5 leads
- `funnel/reportes/2026-07-02.md` — reporte completo
**Total acumulado borrador:** 110 leads (22 corridas)
**Hitos:** San Nicolás de los Arroyos (Buenos Aires) inaugurada ✓ (PBA norte industrial). Venado Tuerto (Santa Fe) inaugurada ✓ (hub sojero SF interior). 110 leads acumulados.

## Corrida anterior (2026-07-01)
**Fecha:** 2026-07-01 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Ushuaia (Tierra del Fuego)** (primera incursión — provincia entera nunca prospectada) + **Necochea (Buenos Aires)** (primera incursión ciudad costera bonaerense)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 5 (CVM ✅ Gmail personal, Rivero ✅ dominio propio, Ushuaia Contable ✅ dominio propio, HAE Dotonianes ✅ dominio propio, Laboranti ✅ email personal)
**Sin email:** 0
**Email status:** 2 verified_personal (CVM Gmail, Laboranti personal), 3 verified_domain (Rivero, Ushuaia Contable, HAE Dotonianes)
**Archivos:**
- `funnel/leads/new/borrador-2026-07-01.jsonl` — 5 leads
- `funnel/reportes/2026-07-01.md` — reporte completo
**Total acumulado borrador:** 105 leads (21 corridas)

## Gotchas descubiertos (continuación — 2026-07-06)
- [2026-07-06] Estudio Contable Pablo Corvalán (Merlo GBA Oeste): Pablo Corvalán CPN, matriculado 2012. Dirección Suipacha 904, Merlo. Email info@estudiocontablecorvalan.com.ar (dominio propio, verificado). Orientado a PyMEs y profesionales: liquidaciones impositivas, sueldos, auditoría, estados contables. El único lead de la corrida con nombre de titular + dominio propio. Candidato ⭐ para primer envío en Merlo.
- [2026-07-06] Estudio Contable Impositivo Sirota (Merlo GBA Oeste, 45+ años): estudio integral con asesoramiento contable, impositivo, laboral, financiero, comercial y societario. Güemes 2132, Merlo. Email estudiocontablesirota@gmail.com (Gmail publicado en sitio oficial). 45+ años de trayectoria = alta cartera. Titular no publicado en web.
- [2026-07-06] Villa / Giménez Estudio Contable (Merlo GBA Oeste): estudio impositivo-contable con asesoramiento jurídico. Bolívar 621 Piso 2 Of. B, Merlo. Email estudiovillagimenez@gmail.com (Gmail publicado en Wix). Nombres de socios no publicados.
- [2026-07-06] Estudio Bonavota (Caseros, Tres de Febrero GBA Oeste): Dra. Patricia Bonavota, fundadora 2013. Especializada en planificación impositiva y liquidación de haberes para PyMEs y unipersonales de CABA y PBA. Av. San Martín 4447, Caseros. Email contacto@estudiobonavota.com.ar (dominio propio, verificado). Candidato ⭐ para primer envío en Tres de Febrero. Ángulo doble carga: SAC + vencimientos Ganancias/BP en simultáneo.
- [2026-07-06] Estudio Buffoni (Caseros, Tres de Febrero GBA Oeste, 40+ años): fundado 1983 por Herbert Buffoni y Nidia Secondini; segunda generación activa: Julieta y Camila Buffoni. Servicios: laboral, societario, impositivo, contable, financiero. Mariano Moreno 4745, Caseros. Email recepcion@estudiobuffoni.com.ar (dominio propio, verificado). Candidato ⭐ para primer envío en Tres de Febrero. Estudio multi-servicio con cartera consolidada.
- [2026-07-06] **Merlo, GBA Oeste:** buen nivel de presencia digital. Varios estudios con sitio web propio y email publicado. Cuidado: "Merlo" devuelve resultados de Villa de Merlo (San Luis) y Morteros (Córdoba) — filtrar por dirección. Fuentes efectivas: licuo.com.ar/merlo, infoisinfo Merlo. Candidatos pendientes para corridas futuras: Estudio Misson (Santos Lugares, info@estudio-misson.com.ar ✓ verificado), otros en CPBA delegación Merlo. Capacidad 10+ corridas.
- [2026-07-06] **Tres de Febrero / Caseros, GBA Oeste:** densidad media de estudios con web propia. Caseros es la cabecera del partido. Otras localidades: Ciudadela, Pablo Podestá, Villa del Parque, Santos Lugares. Candidatos pendientes: Estudio Misson (Santos Lugares, info@estudio-misson.com.ar ✓ verificado). Capacidad 5+ corridas. Fuente: CPBA delegación Tres de Febrero.
- [2026-07-06] **Estudio Misson (Santos Lugares, Tres de Febrero):** email info@estudio-misson.com.ar verificado por agente de búsqueda paralelo. Candidato ⭐ confirmado para próxima corrida en Tres de Febrero.
- [2026-07-06] **HITO: 130 leads en borrador (26 corridas).** Merlo (GBA Oeste) inaugurada ✓. Tres de Febrero/Caseros (GBA Oeste) inaugurada ✓. GBA desagregado: 10 municipios cubiertos. Próximos GBA sugeridos: Tigre/San Fernando (Norte), Pilar (Panamericana Norte), Hurlingham (Oeste), San Isidro (Norte).
- [2026-07-06] **ALERTA TIMING (21 días):** el vencimiento RG ARCA 5851/2026 (27/07/2026) está a 3 semanas. Con 130 leads en Contactos (≥105 con email válido), el warm-up debe iniciarse urgente. Recomendación: flip `OUTREACH_ENABLED=true` inmediatamente + arrancar con los 10 candidatos ⭐ de mayor calidad (Corvalán, Bonavota, Buffoni, Scholiadis, Grasso-Challier, Fulleri, GQM, FCM ISO 9001, Bocco, SAIPE).

## Gotchas descubiertos (continuación — 2026-07-05)
- [2026-07-05] Estudio Contable Scholiadis (Lanús, 40 años, Alberto Scholiadis CPN UBA): email personal Yahoo verificado en sitio propio (scholiadis@yahoo.com.ar). Especialización única del programa: exportación de servicios para artistas y profesionales independientes (Registro de Exportadores de Servicios AFIP, tipo de cambio, monotributo mixto) → doble carga operativa en julio. Candidato ⭐ para primer envío en Lanús.
- [2026-07-05] BMS Contadores Públicos (Lanús Oeste): posicionamiento en outsourcing contable para empresas medianas. Email consultas@ de dominio propio verificado. Nombre de titular no publicado. Servicios: outsourcing, auditoría, impuestos, previsional-laboral, societario. Dirección: Ministro Brin 3039 1° Piso. Ángulo outsourcing = múltiples cierres simultáneos en julio.
- [2026-07-05] Grasso & Challier Asociados (San Andrés, Partido General San Martín, desde 2005): socios Dr. Mariano Martín Grasso + Dr. Pablo Emiliano Challier, ambos en web. Grasso en LinkedIn. Email info@gycasociados.com.ar verificado. Servicio de cálculo de costos y consultoría financiera para PyMEs — diferenciador para el ángulo de automatización. Candidato ⭐ primer envío en General San Martín.
- [2026-07-05] Estudio Profesional San Martín: práctica integral contable-legal con tres áreas diferenciadas (contables@, legales@, consumidor@). Email contables@ verificado. Nombre de titular no publicado. Ángulo único: coordinación simultánea de vencimientos fiscales + plazos judiciales en julio.
- [2026-07-05] Estudio Yusso S.A. (Gerli, Lanús, 40+ años): sitio HTTP 503 durante toda la corrida. Email no extraíble. Estructura societaria con larga trayectoria = cartera consolidada. Candidato para corrida futura (recuperar email vía sitio web cuando vuelva, o CPBA Lanús delegación). Tel: 011 4240-7960.
- [2026-07-05] Alloni, Mica y Asociados (San Martín, CUIT 30-70922439-1 verificado): sin email publicado ni nombre de titular. Dirección: Mitre 3279, San Martín. En múltiples directorios. Candidato para corrida futura vía CPBA General San Martín. Capacidad 5+ corridas adicionales en San Martín.
- [2026-07-05] **Lanús:** buena densidad digital — estudios con sitio web propio y email publicado. Candidatos pendientes: Estudio Yusso (recuperar email), otros en licuo.com.ar/lanus y infoisinfo Lanús. Capacidad 10+ corridas.
- [2026-07-05] **General San Martín:** densidad media — hay estudios con sitio propio pero varios sin email publicado. Fuente efectiva: licuo.com.ar/san-martin + Google. CPBA General San Martín para candidatos sin email. Capacidad 5+ corridas adicionales.
- [2026-07-05] **HITO: 125 leads en borrador (25 corridas).** Lanús (GBA Sur) inaugurada ✓. General San Martín (GBA Norte) inaugurada ✓. GBA desagregado por municipio: 8 municipios cubiertos. Próximos GBA: Merlo (Oeste), Tres de Febrero (Oeste), Tigre/San Fernando (Norte), Pilar (Panamericana Norte).
- [2026-07-05] **Alerta de timing CRÍTICA (semana decisiva):** quedan 22 días para el vencimiento RG ARCA 5851/2026 (27/07/2026). Con 125 leads en Contactos (≥100 con email válido), el warm-up debe iniciarse esta semana. La ventana de máxima urgencia del disparador se cierra en ~2 semanas. Recomendación: flip `OUTREACH_ENABLED=true` + iniciar con los 10 candidatos ⭐ de mayor calidad (Scholiadis, Grasso-Challier, Fulleri, GQM, FCM ISO 9001, Mascheroni, Domínguez, Bocco, SAIPE, Poszler).

## Gotchas descubiertos (continuación — 2026-07-04)
- [2026-07-04] Estudio Fulleri (Avellaneda, 45 años, Dr. Juan Carlos Fulleri): el mejor lead de la corrida ⭐. Email nominativo jfulleri@estudiofulleri.com.ar va directo al Dr. Fulleri (UBA). Servicios: impositivo, auditoría, laboral/previsional, societario, gestión PyMES. Hijo Juan Francisco también activo. Con 45 años + PyMES + auditoría = alta exposición DDJJ julio. Candidato prioritario para primer envío en Avellaneda.
- [2026-07-04] Estudio GQM (Quilmes Oeste): interdisciplinario CPN Hernando Quiñonez Meza + Dra. Ivana Giménez (laboral). 200+ clientes activos. Email contacto@ verificado en sitio propio. Doble perfil contable+jurídico = cartera diversa. Candidato ⭐ para primer envío en Quilmes.
- [2026-07-04] Estudio D'Ambrosio (Quilmes Oeste + Puerto Madero): titular Bernardo D'Ambrosio confirmado en LinkedIn. Doble sede activa. Servicios tributarios, administrativos y auditorías. Email info@ verificado en sitio propio. Ángulo diferenciado: coordinación multi-oficina en pico fiscal.
- [2026-07-04] Gestión Sur (Quilmes Centro): email info@gestionsur.com.ar verificado. Nombre del titular NO publicado en sitio. Llamar al 11-4164-2531 para identificarlo antes del envío real. Especialización en RI + Monotributistas = cartera masiva de vencimientos julio.
- [2026-07-04] Estudio Vitacca y Asociados (Avellaneda, 45 años): email personal Yahoo ivitacca@yahoo.com.ar verificado en sitio propio. Nombre de pila no confirmado (inicial "I"). Llamar al 011-42704478 para confirmar nombre antes del envío real. Especialización agropecuaria = alta exposición DDJJ Ganancias.
- [2026-07-04] Quilmes: alta densidad digital — múltiples estudios con sitio web propio y email publicado. Candidatos pendientes: Estudio Lomazzi (info@estudiolomazzi.com, Rivadavia 25 P4, tel 11-4947-2324), Tambosco Figueroa CP (Almirante Brown 1300), Estudio Santoianni (General Lavalle 865 P1), Estudio Robles (estudiocontablerobles.com.ar), EstudioIlab (Almirante Brown 1405). Capacidad 10+ corridas. Fuentes: infoisinfo-ar.com/quilmes, argentino.com.ar/quilmes.
- [2026-07-04] Avellaneda: buena densidad digital. Candidatos adicionales: Estudio Suárez y Asociados (estudiosuarezyasociados.com — 20+ años), argentino.com.ar/avellaneda lista más estudios. Capacidad 5+ corridas.
- [2026-07-04] **HITO: 120 leads en borrador (24 corridas).** Quilmes (GBA Este) inaugurada ✓. Avellaneda (GBA Sur) inaugurada ✓. GBA desagregado: CABA ✓, La Plata ✓, Lomas de Zamora ✓, Morón ✓, Quilmes ✓, Avellaneda ✓. Próximos GBA sugeridos: Lanús (Sur), Merlo (Oeste), Tres de Febrero (Oeste), San Martín (Norte), Tigre/San Fernando (Norte), Pilar (Norte corredor Panamericana).
- [2026-07-04] **Alerta de timing CRÍTICA:** quedan 23 días para el vencimiento RG ARCA 5851/2026 (27/07/2026). Esta es la última semana de ventana óptima para activar envío real. Con 120 leads en Contactos (≥90 con email válido), el warm-up puede iniciarse hoy con los 10 candidatos ⭐ de mayor calidad. Recomendación urgente: flip `OUTREACH_ENABLED=true` + iniciar con Fulleri, GQM, FCM (ISO 9001), Mascheroni, Domínguez, Bocco, SAIPE.

## Gotchas descubiertos (continuación — 2026-07-03)
- [2026-07-03] Mascheroni & Asociados / Estudio MM (Lomas de Zamora): Marcela Mascheroni, CPN y Lic. en Administración, Técnica en PyMEs. Email info@estudiocontablemm.com.ar verificado en sitio propio. Primer lead de Lomas de Zamora. Ángulo: cartera PyME + pico julio.
- [2026-07-03] Estudio Gattel (Lomas de Zamora, 35 años): Marcela Gattel, email estudiogattel@gmail.com verificado en sitio propio. Servicios societarios, impositivos, sueldos, auditoría. Ángulo: 35 años = cartera consolidada + vencimiento DDJJ julio = pico máximo.
- [2026-07-03] Domínguez & Asociados (Morón): Hernán Domínguez (verificado LinkedIn). Email adm@estudiocontabledominguez.com.ar verificado en página de contacto del sitio. Primer lead de Morón con nombre propio confirmado. Candidato ⭐.
- [2026-07-03] Morgado & Asociados (Morón/CABA/Tandil, fundado 1987): Fernando Morgado (nombre en sección "Nosotros" del sitio). Email info@estudiomorgado.com.ar verificado en sitio propio. Tres sedes: Morón, CABA (Suipacha 280), Tandil (San Martín 348). Especialización agropecuaria. Nota: la sede de Tandil fue identificada como candidata en la corrida 26/06 pero NUNCA se prospectó este estudio — lead válido nuevo. Candidato ⭐ por multi-sede y agro.
- [2026-07-03] Estudio Robledo & Asociados (Morón, fundado 1989, 37 años): especialización diferenciada en agropecuario, cámaras empresariales, cadena cárnica y gestión aduanera. Email contacto@estudiorobledo.com.ar inferido desde snippet Google (sitio 503 al momento de la corrida). Validar antes del envío real. Candidato corrida futura si el sitio vuelve a estar activo.
- [2026-07-03] Lomas de Zamora: mercado de alta densidad digital — múltiples estudios con sitio propio y email publicado. Candidatos pendientes para próximas corridas: Asociados Contables (Azara 597, "3 generaciones", info@asociadoscontables.com.ar, buscar nombre socio vía CPBA Lomas), LAR Estudio Contable (Hipolito Yrigoyen 9792, lar.estudiocontable1@gmail.com), Estudio Zurano (Loria 92 Of. 14, estudiozurano@gmail.com), Estudio Marchesano (sitio propio), Estudio SGN (sitio propio), Lapasset & Asoc (sitio propio). Capacidad 10+ corridas.
- [2026-07-03] Morón: buena densidad de estudios. Candidatos pendientes: Morales y Asociados (WhatsApp, sin email web), Domínguez & Asociados Lorenzo (otro Domínguez, verificar distinción), Estudio Romero Iorio (estudiocontableiorioromero@gmail.com, nombre de socios no publicado). Capacidad 5+ corridas adicionales.
- [2026-07-03] GBA: estrategia de desagregación municipal funciona bien. Próximos municipios sugeridos para corridas futuras: Quilmes (GBA Este), Lanús (GBA Sur), Avellaneda (GBA Sur), Merlo (GBA Oeste), Tres de Febrero (GBA Oeste), San Martín (GBA Norte), Tigre/San Fernando (GBA Norte), Pilar (GBA Norte corredor Panamericana). Cada uno tiene 10+ estudios con sitio web propio.
- [2026-07-03] **Alerta de timing:** quedan 24 días para el vencimiento RG ARCA 5851/2026 (27/07/2026). Esta semana es la ventana ideal para activar el envío real — el disparador está en su punto de máxima urgencia. Recomendación: flip `OUTREACH_ENABLED=true` + iniciar warm-up con los 5-10 candidatos ⭐ de mayor calidad de email.

## Gotchas descubiertos (continuación — 2026-07-02)
- [2026-07-02] Gómez & Faldani (San Nicolás de los Arroyos): dominio propio verificado (gomezfaldani.com.ar), email info@ institucional. Perfil industrial/agro del norte bonaerense — fit perfecto con el disparador de julio. Nombre de pila de socios no publicado en el sitio (investigar LinkedIn o CPBA). Candidato ⭐ para primer envío en San Nicolás.
- [2026-07-02] Bettiolo, Parodi y Lázaro CP (San Nicolás): firma multi-socio en Las Heras 93, presencia web activa, email bloqueado por Cloudflare. Alcance alternativo: guiaurbana.com.ar formulario / tel (0336) 442-5345. Candidato ⭐ para corrida futura con email.
- [2026-07-02] María Cecilia Riccardini (San Nicolás): nombre completo verificado vía TeleXplorer. Don Bosco 361. Tel: (336) 445-4053. Sin email publicado. Candidata corrida futura.
- [2026-07-02] Susana Poszler / Estudio Contable Del Sur (Venado Tuerto): el mejor lead de la corrida ⭐⭐. Email personal Gmail verificado (susanposzler@gmail.com). Sitio propio (estudiocontabledelsur.com) lista activamente los vencimientos de Ganancias, Bienes Personales y Balances — fit perfecto con el disparador. Candidata prioritaria para primer envío en Venado Tuerto. Ángulo: "tu propio sitio publica los mismos vencimientos que motivan este mensaje".
- [2026-07-02] Sandra Edit Peláez (Venado Tuerto): nombre completo + matrícula CPCESF 9.385 verificados, listing Yelp actualizado mayo 2026. Sin email publicado. Alcance alternativo: CPCE Santa Fe delegación Venado Tuerto / tel 034 6243-7846. Candidata corrida futura.
- [2026-07-02] San Nicolás de los Arroyos: primera incursión exitosa. Hub industrial norte bonaerense (~150k hab, Ternium acero + agro). Cloudflare bloquea emails en varios sitios. Fuentes para próximas corridas: guiaurbana.com.ar, telexplorer.com.ar, Páginas Amarillas San Nicolás, CPBA delegación San Nicolás. Capacidad 5+ corridas.
- [2026-07-02] Venado Tuerto (Santa Fe): primera incursión exitosa. Epicentro sojero del sur santafecino (~75k hab). Baja densidad web de estudios contables. Fuentes para próximas corridas: CPCE Santa Fe delegación Venado Tuerto (CPCESF.org.ar), Yelp local, telexplorer.com.ar, argentina.com/venado-tuerto. Capacidad 5+ corridas.
- [2026-07-02] **HITO: 110 leads en borrador (22 corridas).** San Nicolás de los Arroyos (Buenos Aires) inaugurada ✓ (PBA norte industrial). Venado Tuerto (Santa Fe) inaugurada ✓ (hub sojero SF interior). Santa Fe interior: Rafaela ✓, Venado Tuerto ✓.

## Gotchas descubiertos (continuación — 2026-07-01)
- [2026-07-01] Tierra del Fuego (Ushuaia): primera incursión exitosa — provincia completamente virgen para propuestas tech. Ángulo diferencial único: régimen promocional Ley 19.640 (zona franca industrial) = doble complejidad impositiva para los estudios fueguinos (DDJJ nacionales + exenciones/alícuotas diferenciales TdF + clientes con facturación en divisas). Baja saturación de propuestas digitales = diferenciador real. Capacidad para 10+ corridas (Ushuaia + Río Grande).
- [2026-07-01] Rivero y Asociados (Ushuaia): estudio con especialización explícita en tokenización y facturación en moneda extranjera. Email info@riveroyasociados.com.ar verified. Fundador: Alejandro Rivero (UNPSJB). Ángulo tech-adjacent: "ya asesorás en cripto, OPTIMIZAR es la automatización que le sigue". Candidato ⭐ para primer envío en TdF.
- [2026-07-01] Estudio Contable CVM (Ushuaia): unipersonal, 13 años. CP. Cecilia Von Mundhardt. Email cvmestudio@gmail.com verified. Candidato ⭐ para primer envío en TdF (ángulo unipersonal = máxima urgencia en julio).
- [2026-07-01] Ushuaia Contable: fundada 2009, equipo de 4 (Dalila, Eliana, Esteban, Ignacio). Apellido de Eliana (socia fundadora) no publicado — investigar vía CPCE TdF (cpce-tf.org.ar) o LinkedIn. Email info@ushuaiacontable.com.
- [2026-07-01] Estudio Laboranti (Necochea): perfil multidisciplinario (contable + tributario + legal + comunicación). Andrea Laboranti, email andrea@laboranti.com.ar verified personal. Primera Necochea del programa.
- [2026-07-01] HAE Dotonianes (Necochea): estudio orientado a planificación tributaria PyMEs. Email estudio@haedotonianes.com. Nombre de titular no publicado — investigar vía CPBA Necochea (dlgnecochea@cpba.com.ar / Calle 57 Nº 2745).
- [2026-07-01] Río Grande (TdF): no se encontraron emails verificados esta corrida. Candidatos para próximas corridas: Estudio Contable Lanza (B de O'Higgins 156), Estudio Santa Cruz (Alberdi 1019), Vidal M & Orlando R (9 de Julio 790), Edgardo Benvenuto (Alberdi 883), Dragani Nora E (L Rosales 256), Cr. Luis Luciuk. Fuente: guia-tierra-del-fuego.miguiaargentina.com.ar.
- [2026-07-01] Necochea: hub pesquero-agroindustrial bonaerense (~90k hab). Primera incursión exitosa. Otros candidatos: Estudio Crasso (Lucio Crasso, 40+ años, email en estudiocrasso.com.ar — bloqueado hoy), C y D Estudio (recepcion@cydestudio.com — sitio 503), Jorge Balbi (Calle 44 2795), Dr. Laguezza (Calle 63 2748). Fuente: necochea.licuo.com.ar (8 resultados).
- [2026-07-01] CPCE Tierra del Fuego: cpce-tf.org.ar — fuente para corridas futuras en Ushuaia y Río Grande. Presidente: Dr. Heraclio J. Lanza (Río Grande, O'Higgins 133, tel 02964 422061, cpce@cpce-tdf.org.ar).

## Corrida anterior (2026-06-30)
**Fecha:** 2026-06-30 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **San Rafael (Mendoza)** (primera incursión Mendoza interior, hub vitivinícola/agro) + **Olavarría (Buenos Aires)** (primera incursión PBA centrosur agroindustrial)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 4 (Pagliano ✅ Gmail verificado CUIT, Estudio AG ✅ dominio propio inferred, ECOAG ✅ Gmail inferred, Ibarlucía ✅ Gmail verificado sitio)
**Sin email:** 1 (Secondi — not_found; clientes corporativos Arcor/Loma Negra/La Serenísima ⭐)
**Email status:** 2 verified_personal (Pagliano Gmail CUIT ✓, Ibarlucía Gmail sitio ✓), 1 inferred_domain (Estudio AG info@), 1 inferred_personal (ECOAG Gmail visible en sitio), 1 not_found
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan 27 días
**Archivos:**
- `funnel/leads/new/borrador-2026-06-30.jsonl` — 5 leads
- `funnel/reportes/2026-06-30.md` — reporte completo
**Total acumulado borrador:** 100 leads (20 corridas) — **HITO: 100 LEADS**
**Hitos:** San Rafael (Mendoza) inaugurada ✓. Olavarría (Buenos Aires) inaugurada ✓. Mendoza interior abierto ✓. PBA centrosur abierto ✓. **Hito 100 leads (20 corridas).**
**Próximo bloqueante:** Validar calidad de los emails y activar envío real (`OUTREACH_ENABLED=true` + warm-up). Candidatos prioritarios ⭐: Bocco (Villa María, dominio propio, agro), SAIPE (multi-sucursal, email personal alfiore@), LS S.A. (José Sasia, 70 años), Marturet (Concordia), Carnevale (Pergamino), Fernández Carrera Molejón (ISO 9001, General Roca ⭐⭐), Pagliano (San Rafael, Gmail CUIT verificado). Candidatos sin email para corrida futura: Secondi ⭐ (Olavarría, corporativo, CPBA), Fernandez Tesone ⭐ (Gualeguaychú, +200 empresas, CPCE ER), Alvarez & Asociados ⭐ (Villa María, 40 años, CPCE Córdoba), Massari ⭐ (Junín, CPBA).

## Corrida anterior (2026-06-29)
**Fecha:** 2026-06-29 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Villa María (Córdoba)** (primera incursión Córdoba interior 2ª ciudad) + **Gualeguaychú (Entre Ríos)** (primera incursión — completa Entre Ríos)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 3 (Barceló ✅ personal Yahoo, Bocco ✅ dominio propio ⭐, Ronconi ✅ Gmail verificado)
**Sin email:** 2 (Alvarez & Asociados — not_found, sitio 503; Fernandez Tesone — not_found ⭐, +200 empresas)
**Email status:** 1 verified_domain (Bocco ⭐), 2 verified_personal (Barceló Yahoo, Ronconi Gmail), 2 not_found
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan 28 días
**Archivos:**
- `funnel/leads/new/borrador-2026-06-29.jsonl` — 5 leads
- `funnel/reportes/2026-06-29.md` — reporte completo
**Total acumulado borrador:** 95 leads (19 corridas)
**Hitos:** Villa María (Córdoba) inaugurada ✓. Gualeguaychú (Entre Ríos) inaugurada ✓. Entre Ríos completa: Paraná ✓, Concordia ✓, Gualeguaychú ✓. Córdoba interior: Río Cuarto ✓, Villa María ✓.

## Corrida anterior (2026-06-28)
**Fecha:** 2026-06-28 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Rafaela (Santa Fe)** (primera incursión) + **Junín (Buenos Aires)** (primera incursión PBA noroeste agroindustrial)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 3 (SAIPE ✅ dominio propio ⭐, LS S.A. ✅ dominio propio ⭐, Ayuste ✅ dominio propio personal)
**Sin email:** 2 (Massari — not_found, Balbi-Bergamini — not_found; Junín tiene baja presencia digital — investigar vía CPBA Junín)
**Email status:** 3 verified dominio propio (SAIPE, LS S.A., Ayuste), 2 not_found (Massari, Balbi-Bergamini)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan 29 días
**Archivos:**
- `funnel/leads/new/borrador-2026-06-28.jsonl` — 5 leads
- `funnel/reportes/2026-06-28.md` — reporte completo
**Total acumulado borrador:** 90 leads (18 corridas)
**Hitos:** Rafaela Santa Fe inaugurado ✓. Junín Buenos Aires inaugurado ✓ (mercado de baja presencia digital — estrategia CPBA para próximas corridas). Hito 90 leads (18 corridas).

## Corrida anterior (2026-06-27)
**Fecha:** 2026-06-27 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Concordia (Entre Ríos)** (primera incursión Entre Ríos interior) + **Pergamino (Buenos Aires)** (primera incursión PBA agrícola norte)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 4 (Narbais ✅ arnetbiz ISP, Azambuya ✅ Gmail, Marturet ✅ dominio propio ⭐, Carnevale ✅ dominio propio ⭐)
**Sin email:** 1 (Selmi — not_found; sin nombre socio publicado; investigar CPCE PBA Pergamino o LinkedIn)
**Email status:** 2 verified dominio propio (Marturet, Carnevale), 1 ISP (Narbais arnetbiz), 1 Gmail (Azambuya), 1 not_found (Selmi)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) — quedan 30 días
**Archivos:**
- `funnel/leads/new/borrador-2026-06-27.jsonl` — 5 leads
- `funnel/reportes/2026-06-27.md` — reporte completo
**Total acumulado borrador:** 85 leads (17 corridas)
**Hitos:** Entre Ríos interior inaugurado (Concordia ✓). PBA agrícola norte inaugurado (Pergamino ✓).
**Próximo bloqueante:** Validar calidad de los emails y activar envío real (`OUTREACH_ENABLED=true` + warm-up). Candidatos prioritarios ⭐: Marturet (Concordia, 14 profes, dominio propio), Carnevale (Pergamino, 50 años, dominio propio), Fernández Carrera Molejón (ISO 9001, General Roca, verified ⭐⭐), Toloza (Formosa, verified), CILS/Chinellato (Bariloche, verified). Candidatos sin email para corrida futura: Selmi ⭐ (Pergamino, CPCE PBA), López Madina ⭐ (Tandil, CPCE PBA), Símaro Torchelli ⭐⭐ (Tandil, site 503), García ⭐ (SdE, CPCE), Bonino ⭐ (San Luis, CPCE), Melnik ⭐⭐ (Catamarca, CPCE), Rojas Naser ⭐⭐ (Jujuy, CPCE), Magnago ⭐ (Río Cuarto, CPCE Córdoba).

## Corrida anterior (2026-06-26)
**Fecha:** 2026-06-26 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Tandil (Buenos Aires)** (primera incursión PBA interior) + **General Roca (Río Negro)** (primera incursión Patagonia Centro-Norte / Alto Valle)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado) | Sitios caídos descartados: Símaro Torchelli (503), Robles & Asociados (403), RGA (resultó ser CABA)
**Emails escritos:** 4 (ARHEX ✅ dominio propio, Gustavo López ✅ dominio propio, Fernández Carrera Molejón ✅ dominio propio ⭐⭐, Wendy Apcarian ✅ dominio propio)
**Sin email:** 1 (López Madina — not_found; sitio 503 durante la corrida; investigar CPCE PBA Tandil)
**Email status:** 4 verified dominio propio, 1 not_found
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026)
**Archivos:**
- `funnel/leads/new/borrador-2026-06-26.jsonl` — 5 leads
- `funnel/reportes/2026-06-26.md` — reporte completo
**Total acumulado borrador:** 80 leads (16 corridas)
**Hitos:** PBA interior inaugurado (Tandil ✓). Patagonia Centro-Norte inaugurada (General Roca/Alto Valle ✓). 80 leads = hito de escala.

## Gotchas descubiertos (continuación — 2026-06-27)
- [2026-06-27] Consultora Marturet (Concordia, ER, desde 1982, 14 profesionales): mayor equipo de la corrida. Email contacto@consultoramarturet.com.ar verified. Ángulo multiplicador: cada hora automatizada se multiplica por 14. Candidato ⭐ para primer envío en Concordia.
- [2026-06-27] Estudio Carnevale (Pergamino, BA, desde 1975): primer estudio del programa en Pergamino. Email info@estudiocarnevale.com verified. 50 años de trayectoria = alto volumen de clientes PyME = muchos procesos optimizables. Candidato ⭐ para primer envío en Pergamino.
- [2026-06-27] Narbais & Asociados (Concordia, ER, 30+ años): especializado en PyMEs y sociedades agrarias. Email estudionarbais@arnetbiz.com.ar (arnetbiz = ISP Telecom/Arnet, similar deliverability a dominio propio). Validar mailbox activo antes del envío real.
- [2026-06-27] Morera-Azambuya & Asociados (Concordia): perfil triple contable+jurídico+laboral, tres socios (Morera, Azambuya, Zalisñak). Email Gmail — deliverability estándar. Ayelén Azambuya es la contacto más accesible web.
- [2026-06-27] Selmi & Asociados (Pergamino): 20+ años, sin nombre de socio ni email públicos. Fuente solo Páginas Amarillas. Investigar vía CPCE Buenos Aires delegación Pergamino o LinkedIn para corrida futura.
- [2026-06-27] Concordia, Entre Ríos: primera incursión exitosa. Segunda ciudad de ER (~150k hab), hub citrícola-agrícola. Baja exposición tech = diferenciador real. Capacidad para 5+ corridas adicionales. Candidatos pendientes: otros estudios del directorio licuo.com.ar/concordia, CPCE ER delegación Concordia.
- [2026-06-27] Pergamino, Buenos Aires: primera incursión exitosa. Hub agrícola norte bonaerense (~100k hab). Ángulo DDJJ + Bienes Personales es especialmente potente en zonas agropecuarias (muchos clientes con campo/acciones). Capacidad para 5+ corridas adicionales.
- [2026-06-27] Hito: 85 leads en borrador (17 corridas). Entre Ríos interior inaugurado (Concordia ✓). PBA agrícola norte inaugurado (Pergamino ✓).

## Gotchas descubiertos (continuación — 2026-06-26)
- [2026-06-26] Fernández Carrera Molejón (General Roca, ISO 9001): segundo estudio con certificación ISO del programa (el primero fue Contadores Rosario). Eduardo Fernández Carrera (UNComahue + Master EIN) y Andrea Molejón (UNQuilmes + Coach Ontológico). Email fcm@fernandezcarreramolejon.com.ar verified. Ángulo diferenciado único: "ISO 9001 = procesos documentados → OPTIMIZAR los automatiza". Candidato ⭐⭐ para primer envío real en General Roca.
- [2026-06-26] ARHEX (Tandil, desde 1973): 51 años de trayectoria + servicios de criptomonedas. Doble matrícula CPCECABA y CPCEPBA. Primer estudio del programa que ofrece criptomonedas explícitamente. Ángulo complementario: "la automatización que va por encima del accounting de cripto". Email info@estudioarhex.com.ar verified.
- [2026-06-26] Símaro Torchelli (Tandil, desde 1992): el estudio más consolidado de Tandil (multi-sucursal: Tandil, Buenos Aires, Azul, Olavarría, Bolívar, Juárez). Sitio 503 durante toda la corrida. Nombre completo: Othar Símaro + Torchelli. CUIT: 30-71749744-5. Candidato ⭐⭐ para corrida futura.
- [2026-06-26] López Madina SRL (Tandil): Patricio López Madina CPN, clientes en agro/industria del centro bonaerense (Grupo Ceres Tolvas). Sitio 503, email no publicado. Candidato ⭐ para corrida futura vía CPCE PBA Tandil o LinkedIn.
- [2026-06-26] Tandil tiene capacidad para 5+ corridas adicionales: Símaro Torchelli ⭐⭐, López Madina ⭐, AD Estudio (ENOTFOUND), Morgado branch (San Martín 348), Estudio LMA (tres contadoras, tel +54 9 249 462 4664, sin email web), Estudio Rosales & Asoc (Facebook).
- [2026-06-26] General Roca tiene 49+ estudios en directorio SoyCiudad. Capacidad para 10+ corridas. Candidatos inmediatos: Ariel Lodosky (Canada 703, tel 0298-4421433), Neiman Fernández (Mendoza 1119, tel 0298-442-6702), N&M Contadores Públicos (JF Kennedy 1765), Robles & Asociados (403 hoy), Eduardo Roca (30+ años, sin email web).
- [2026-06-26] Wendy Apcarian: email alternativo de Franco Ghirardelli (jefe contable): contable@estudiowendy.com.ar. Usar si recepcion@ no responde.
- [2026-06-26] Hito: 80 leads en borrador (16 corridas). PBA interior inaugurado (Tandil ✓). Patagonia Centro-Norte inaugurada (General Roca/Alto Valle ✓).

## Corrida anterior (2026-06-25)
**Fecha:** 2026-06-25 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Río Cuarto (Córdoba)** (primera incursión Córdoba interior) + **Río Gallegos (Santa Cruz)** (primera incursión Patagonia Sur)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado) | 1 descartado de la búsqueda: Manzanares Montane Pombo (Río Gallegos, riesgo reputacional — contador Kirchner)
**Emails escritos:** 4 (Scapin ✅, Dalio ✅, Borquez ⚠️ Gmail, Van Thienen ✅)
**Sin email:** 1 (Magnago — not_found; investigar CPCE Córdoba)
**Email status:** 2 verified dominio propio (Scapin, Van Thienen), 1 verified dominio propio (Dalio), 1 inferred Gmail (Borquez), 1 not_found (Magnago)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026)
**Archivos:**
- `funnel/leads/new/borrador-2026-06-25.jsonl` — 5 leads
- `funnel/reportes/2026-06-25.md` — reporte completo
**Total acumulado borrador:** 75 leads (15 corridas)
**Hitos:** Patagonia Sur inaugurada (Río Gallegos/Santa Cruz ✓). Córdoba interior inaugurado (Río Cuarto ✓).
**Próximo bloqueante:** Validar calidad de los emails y activar envío real (`OUTREACH_ENABLED=true` + warm-up). Candidatos prioritarios ⭐⭐: Toloza (Formosa, verified, contenido fiscal propio), CILS/Chinellato (Bariloche, verified, perfil tech-adjacent PIT). Candidatos sin email para corrida futura: García ⭐ (SdE, CPCE), Bonino ⭐ (San Luis, CPCE), Melnik ⭐⭐ (Catamarca, CPCE), Rojas Naser ⭐⭐ (Jujuy, CPCE), Magnago ⭐ (Río Cuarto, CPCE Córdoba).

## Gotchas descubiertos (continuación — 2026-06-25)
- [2026-06-25] Scapin & Asociados (Río Cuarto): software contable propio para agro/industria/servicios. Ángulo diferenciado: "la automatización que va por encima del software que ya usan". Email dominio propio verificado. Candidato ⭐.
- [2026-06-25] Río Cuarto (Córdoba): segunda ciudad de la provincia, capacidad para 10+ corridas. Candidatos pendientes: Magnago (email pendiente CPCE Córdoba ⭐), Battaglino (agropecuario, Facebook), Rambaldi, Boccolini (Paunero 481), SM & Asociados (María Olguín 739). Fuente: telexplorer.com.ar, argentino.com.ar.
- [2026-06-25] Río Gallegos (Santa Cruz): mercado poco saturado de propuestas tech. Primera incursión exitosa. Candidatos adicionales: Ovando (Sarmiento 143), A Y S Soc (Estrada 140), Luigi Braim CPN (9 de Julio 370), Palicio-Spitaleri (Gdor. Lista 436). Fuente: licuo.com.ar/santa-cruz, infoisinfo rio-gallegos.
- [2026-06-25] Van Thienen (Río Gallegos): allanado en 2023 por causa binacional Argentina-Chile (lavado/contrabando/drogas). Titular declaró inocencia. Verificar resolución de la causa antes del envío real.
- [2026-06-25] Manzanares Montane Pombo (Río Gallegos): DESCARTADO permanentemente — Víctor Manzanares es contador de la familia Kirchner, detuvo 2017. Riesgo reputacional inaceptable.
- [2026-06-25] Hito: 75 leads en borrador (15 corridas). Patagonia Sur inaugurada (Río Gallegos/Santa Cruz ✓).

## Gotchas descubiertos (continuación — 2026-06-24)
- [2026-06-24] Toloza (Formosa Capital): perfil de adoptador temprano — publica contenido propio de actualización fiscal (SAS, reforma laboral, wallets digitales 2026). Email hugotoloza@yahoo.com.ar verified en su web Wix. Candidato ⭐ para primer envío real en Formosa. Ángulo: "ya publicás sobre wallets y SAS — OPTIMIZAR es la automatización que le sigue".
- [2026-06-24] CILS / Javier Chinellato (Bariloche): figura en el Parque Productivo Tecnológico Industrial de Bariloche (PIT) — sugiere clientela tech/industrial. Socio Gerente confirmado en LinkedIn. Email info@estudiocils.com.ar verified. Candidato ⭐⭐ — mejor lead de Bariloche. Ángulo diferenciado: "la automatización que usan tus clientes tech, ahora para tu propio estudio".
- [2026-06-24] CGD - Cremer, González, Deza (Bariloche, desde 2005): 20 años, equipo diverso, servicios de auditoría/impuestos/laboral/finanzas. Email info@estudiocgd.com.ar verified. Activo en RRSS. Candidato ⭐ sólido.
- [2026-06-24] Formosa Capital: baja densidad de estudios con web propia (mercado poco saturado por propuestas tech — igual que La Rioja y SdE). Candidatos para corridas futuras: Estudio Álvarez (alvarez_estudio@hotmail.com verified, buscar nombre socio vía CPCE Formosa o LinkedIn), Estudio Eunise Aranda (J.J. Castelli 944, sin email), Estudio H&G (Junín 36, sin email). Fuente: licuo.com.ar/formosa + infoisinfo-ar.com.
- [2026-06-24] Bariloche: mercado con capacidad para 10+ corridas adicionales. Candidatos: Estudio MG (Neuquén 1060), Martínez González y Asociados. Fuentes: licuo.com.ar, soyciudad, guiamaster Bariloche.
- [2026-06-24] Hito: 70 leads en borrador (14 corridas). NEA completo: Chaco ✓, Misiones ✓, Corrientes ✓, Formosa ✓. Patagonia Norte inaugurada: Bariloche/Río Negro ✓.

## Gotchas descubiertos (continuación — 2026-06-23)
- [2026-06-23] Corrientes Capital: primera incursión exitosa tras dos intentos fallidos (06-18 y 06-19 — postergado). Fuente clave que funcionó: ciudad-de-corrientes.licuo.com.ar + az-argentina.com + búsquedas de webs propias. Los 3 emails son inferred (sitios web caídos al momento de la corrida).
- [2026-06-23] Estudio Leiva (Corrientes, H. Yrigoyen 1364): Cr. Humberto Ariel Leiva, MP 2658, 15+ años de experiencia, servicios contable/impositivo/laboral para PyMEs. Email contabilidad@estudioleiva.com (inferred, sitio 503). Primer candidato de Corrientes.
- [2026-06-23] Estudio Pizzichini (Corrientes, 9 de Julio 1691): Cr. José Luis Pizzichini, email luis_pizzi@hotmail.com (inferred desde estudiopizzichini.com, ECONNREFUSED). Segundo Corrientes.
- [2026-06-23] Estudio Contable San Martin (Corrientes): email sanmartin2130@gmail.com (Gmail, inferred), tel +54 379 477-9289. Nombre del titular no encontrado — corrida futura via CPCE Corrientes o LinkedIn.
- [2026-06-23] Santiago del Estero Capital: segunda ciudad del programa con muy baja presencia web (similar a La Rioja). La mayoría de estudios no tiene sitio propio ni email publicado. Fuente más prometedora: CPCE SE (cpcese.org.ar/matriculados/padron — público, sin login). Candidato prioritario: Cr. Mario Nicolás García ⭐ (60+ clientes, doble titulación UNC+UNT, Congreso 10 esq. Belgrano).
- [2026-06-23] Estudio Facello Palavecino y Asociados (SdE, San Martín 209): estudio contable + jurídico. Sin email publicado. Candidato para corrida futura vía CPCE SdE o LinkedIn.
- [2026-06-23] CPCE Santiago del Estero: presidente Cp. Jorge NEME. El padrón de matriculados es público (cpcese.org.ar/matriculados/padron) — tiene centenas de entradas alfabéticas. Fuente para corridas futuras en SdE.
- [2026-06-23] Corrientes Capital tiene capacidad para 5+ corridas adicionales. Candidatos: Menegaz-Urbani (Av. Gdor. Ruiz), Spessot Gilberto (Salta 648), Estudio Leiva (email inferred, validar), Estudio Franco (Pje A González 1009), Estudio Olivarez y Asoc (La Rioja 840). Fuente: licuo + telexplorer Corrientes.
- [2026-06-23] Santiago del Estero Capital tiene capacidad para 5+ corridas. Candidatos: Estudio Nasif Rodríguez (Moreno Sur 211), Estudio Arce & Asociados (Libertad 761), Estudio Díaz Yocca (24 de Septiembre 257), Estudio Simonetti (24 de Septiembre 262, simonetti-net.com.ar 503), Estudio Bravo (Avellaneda 292, estudiojdbravo.com.ar ECONNREFUSED). Fuente: telexplorer.com.ar.
- [2026-06-23] Hito: 65 leads en borrador (13 corridas). Corrientes inaugurada ✓. Santiago del Estero inaugurada ✓.

## Corrida anterior (2026-06-22)
**Fecha:** 2026-06-22 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **Córdoba Capital (segundo lote)** + **Comodoro Rivadavia, Chubut (primera incursión Patagonia Sur)**
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 4 (OCAR: dominio propio ✅, Estudio Contable Córdoba: dominio propio ✅, Koroluk: dominio propio ✅ ⭐⭐, Barria&Perea: dominio propio ✅)
**Sin email:** 1 (Peinó — modelo remoto, candidato ⭐ corrida futura vía LinkedIn)
**Email status:** 4 verificados dominio propio (OCAR, Estudio Contable Córdoba, Koroluk, Barria&Perea), 1 not_found (Peinó)
**Disparador:** Prórroga DDJJ Ganancias/Bienes Personales período 2025 hasta 27/07/2026 (RG ARCA 5851/2026) + ángulo Oil & Gas / Patagonia para Koroluk (65+ clientes energéticos)
**Archivos:**
- `funnel/leads/new/borrador-2026-06-22.jsonl` — 5 leads
- `funnel/reportes/2026-06-22.md` — reporte completo
**Total acumulado borrador:** 60 leads (12 corridas)
**Próximo bloqueante:** Validar calidad de emails y activar envío real (`OUTREACH_ENABLED=true` + warm-up). Prioridad emails personales verificados: Libran ⭐⭐ (La Plata, dominio propio), Bisonni ⭐⭐, Herusa, Pereiro (06-17), Betique (06-16), Torre-Pulisich (06-13), Farina (06-13). Candidatos sin email para corrida futura: Peinó ⭐ (Córdoba, LinkedIn), Bonino ⭐ (San Luis, CPCE), Melnik ⭐⭐ (Catamarca, CPCE), Rojas Naser ⭐⭐ (Jujuy, CPCE).

## Gotchas descubiertos (continuación — 2026-06-22)
- [2026-06-22] OCAR (Córdoba, desde 1942): estudio con 80+ años, cartera empresarial de élite, email ocar@ocar.com.ar (dominio propio). Socios: Gustavo Bagur (UNC) + Ricardo Viano (UCC). Servicios de alto nivel: due diligence, valuación, fusiones. También outsourcing + payroll → ángulo de automatización de procesos propios. Candidato ⭐ para primer envío en Córdoba 2° lote.
- [2026-06-22] Koroluk, García Gavuzzo y Asociados (Comodoro Rivadavia): 4 profesionales, 65+ empresas clientes en Oil & Gas, transporte y retail. Email impuestos@estudiokg.com.ar (dominio propio). Ángulo diferenciado: el volumen de liquidaciones impositivas en plaza petrolera es significativamente mayor que en estudios de servicios estándar. Candidato ⭐⭐ — mejor lead de Comodoro.
- [2026-06-22] Fernando Peinó (Córdoba): CPN + Master Dirección de Negocios UNC, modelo 100% remoto, SAS, tax planning estratégico. Sin email publicado (solo WhatsApp/Instagram). Perfil tech-adjacent muy similar a Bisonni ⭐⭐ y Dutto. Buscar email vía LinkedIn o formulario en corrida futura.
- [2026-06-22] Estudio Guerrero (Córdoba, Raymond Poincaré 7154): socios publicados (Santiago Guerrero, Lucía Lopez, Gianna Fontana, Carla Keuchguerian, Lucila Veliz). Sitio 503 durante la corrida. Candidato para corrida futura cuando el sitio esté accesible.
- [2026-06-22] Comodoro Rivadavia: primera incursión completada. Mercado con perfil Oil & Gas → ángulo diferenciado (volumen + complejidad de clientes energéticos). Candidatos para próximas corridas: Ferreyra (soluciones@estudiocontableferreyra.com.ar), Rayleff (Daniel Rayleff, Gmail), GM Estudio Contable (gmestudiocontable.com). Fuentes: licuo.com.ar/comodoro-rivadavia, telexplorer.com.ar.
- [2026-06-22] Barria & Perea (Comodoro): email estudio@barriayperea.com.ar (dominio propio). Nombre de socios no publicado. Investigar via CPCE Chubut o LinkedIn antes del envío real para personalizar.
- [2026-06-22] Córdoba Capital: ahora con 10 leads (corridas 11/06 y 22/06). Capacidad para 15+ corridas adicionales. Próximas fuentes: Estudio Guerrero (cuando el sitio esté accesible), Dominguez y Asoc (ECONNREFUSED hoy), CPCE Córdoba directorio.
- [2026-06-22] Hito: 60 leads en borrador (12 corridas). Patagonia Sur inaugurada (Comodoro Rivadavia ✓).

## Corrida anterior (2026-06-21)
**Fecha:** 2026-06-21 | **Modo:** BORRADOR (sin envíos reales)
**Segmento:** Estudios contables/impositivos — **La Plata** (capital PBA — primera incursión) + **San Luis Capital** (primera incursión — completa cinturón Cuyo)
**Cupo usado:** 5 leads
**Leads encontrados:** 5
**Leads descartados:** 0 (ninguno en La Pampa; ningún duplicado)
**Emails escritos:** 4 (Castaños: dominio propio ✅, Libran: personal ⭐⭐, Enfoque: Gmail, Moreno Chediack: dominio propio ✅)
**Sin email:** 1 (Bonino ⭐ — Vocal CPCE San Luis, candidata prioritaria)
**Archivos:**
- `funnel/leads/new/borrador-2026-06-21.jsonl` — 5 leads
- `funnel/reportes/2026-06-21.md` — reporte completo
**Total acumulado borrador:** 55 leads (11 corridas)

## Gotchas descubiertos (continuación — 2026-06-21)
- [2026-06-21] Estudio Contable Libran (La Plata): Cra. Liliana Patricia Libran, en ejercicio desde 1982, email personal en dominio propio (liliana@estudiolibran.com.ar). Mejor candidata de esta corrida ⭐⭐. Monotributistas, autónomos, PyMEs → base de clientes amplia.
- [2026-06-21] Enfoque Contable (La Plata): único estudio del programa que vende CFO Fraccionado como servicio. Fundadores UNLP (Rodríguez + Bizet). Perfil tech-adjacent similar a Bisonni (BI) y Dutto (servicios informáticos). Ángulo recomendado: "la automatización es lo que viene después del CFO Fraccionado". Email Gmail.
- [2026-06-21] Eleonora Bonino (San Luis): tercer candidato con perfil CPCE Vocal de todo el programa (Rojas Naser ⭐⭐ Jujuy, Melnik ⭐⭐ Catamarca). Patrón confirmado: Vocales de CPCE = adoptadores tempranos de alta probabilidad. Investigar email en corrida futura vía cpcesanluis.org.ar/Matriculados.
- [2026-06-21] San Luis Capital: baja presencia web de estudios (similar a La Rioja). CPCE San Luis (cpcesanluis.org.ar) devolvió 503 durante la corrida. Para corridas futuras: Estudio San Blas (9 de Julio y San Martín), Estudio Bustos & Asociados, Villegas-Temoli (Anacleto Toesca 1889), Dra. Reinaldo (Rivadavia 1305).
- [2026-06-21] La Plata tiene capacidad para 10+ corridas adicionales. Candidatos: Bordagaray y Asociados (20+ años), CSD y Asociados (40+ años, 403), Estudio García (25+ años, La Plata + CABA), Andrea Ducar Contadora, Estudio Paredes.
- [2026-06-21] Cuyo completo: Mendoza ✓, San Juan ✓, San Luis ✓. Hito geográfico.
- [2026-06-21] Decisiones tomadas: La Plata (primera incursión PBA capital provincial) + San Luis Capital (completa Cuyo). 5/5 × 200 al CRM. Total: 55 leads (11 corridas).

## Corrida anterior (2026-06-20)
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
