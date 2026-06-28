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
- Corridas borrador completadas: 11/06 (Córdoba/Rosario), 12/06 (CABA/GBA), 13/06 (Mendoza/Tucumán), 14/06 (Salta/Mar del Plata), 15/06 (Bahía Blanca/Neuquén), 16/06 (Santa Fe/Paraná), 17/06 (Rosario expansión), 18/06 (San Juan/Resistencia Chaco), 19/06 (Jujuy/Posadas Misiones), 20/06 (La Rioja Capital/Catamarca Capital), 21/06 (La Plata/San Luis Capital), 22/06 (Córdoba 2° lote/Comodoro Rivadavia), 23/06 (Corrientes Capital/Santiago del Estero Capital), 24/06 (Formosa Capital/Bariloche Río Negro), 25/06 (Río Cuarto/Río Gallegos Santa Cruz), 26/06 (Tandil/General Roca Río Negro), 27/06 (Concordia Entre Ríos/Pergamino Buenos Aires), 28/06 (**Rafaela Santa Fe/Junín Buenos Aires**) → **90 leads en borrador (18 corridas)**. Cinturón NOA completo (Mendoza, Tucumán, Salta, Jujuy, La Rioja, Catamarca, Santiago del Estero ✓). Cuyo completo (Mendoza, San Juan, San Luis). Patagonia: Neuquén ✓, Comodoro ✓, Bariloche ✓, Río Gallegos ✓, General Roca ✓. NEA completo: Chaco ✓, Misiones ✓, Corrientes ✓, Formosa ✓. Córdoba interior: Río Cuarto ✓. PBA interior: Tandil ✓, Pergamino ✓, **Junín ✓**. Entre Ríos interior: Concordia ✓. Santa Fe interior: **Rafaela ✓**.
- Pendiente real: validar calidad de los emails y, cuando se apruebe, encender el envío (flip a push-vivo).

## Última corrida
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
**Próximo bloqueante:** Validar calidad de los emails y activar envío real (`OUTREACH_ENABLED=true` + warm-up). Candidatos prioritarios ⭐: SAIPE (multi-sucursal, email personal alfiore@), LS S.A. (José Sasia, 70 años), Marturet (Concordia), Carnevale (Pergamino), Fernández Carrera Molejón (ISO 9001, General Roca ⭐⭐). Candidatos sin email para corrida futura: Massari ⭐ (Junín, CPBA), Balbi-Bergamini ⭐ (Junín, CPBA), Di Prinzio (Junín, CPBA), Selmi ⭐ (Pergamino, CPCE PBA), López Madina ⭐ (Tandil, CPCE PBA).

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
