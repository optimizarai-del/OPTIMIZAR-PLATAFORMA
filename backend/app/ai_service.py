import os
import json
import httpx
from typing import List, Dict, Optional

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-4-5-20251001"


def _call_claude(prompt: str, max_tokens: int = 2048) -> Dict:
    """
    Llama a Claude. Devuelve {"ok": bool, "data": dict | None, "error": str | None}.
    Espera que Claude responda con JSON puro.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        return {"ok": False, "data": None, "error": "ANTHROPIC_API_KEY no configurada en backend/.env"}

    try:
        resp = httpx.post(
            ANTHROPIC_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": MODEL,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=60,
        )
        resp.raise_for_status()
        raw = resp.json()["content"][0]["text"].strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```", 2)[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()
        return {"ok": True, "data": json.loads(raw), "error": None}
    except json.JSONDecodeError as e:
        return {"ok": False, "data": None, "error": f"Error al parsear respuesta IA: {e}"}
    except httpx.HTTPStatusError as e:
        return {"ok": False, "data": None, "error": f"API Anthropic {e.response.status_code}: {e.response.text[:200]}"}
    except Exception as e:
        return {"ok": False, "data": None, "error": f"Error IA: {e}"}


# ── 0. Matching requerimiento ↔ catálogo de servicios ─────────────────────────

# Palabras muy comunes que no aportan a un match real (evitan falsos positivos).
# Incluye stopwords de 3 letras porque bajamos el mínimo a 3 chars para captar
# acrónimos discriminantes del dominio (AFIP, CAE, PDF, IVA, CRM, ERP, API, BOT).
_STOPWORDS = {
    "los", "las", "con", "por", "una", "uno", "del", "que", "sus", "mas", "muy",
    "son", "fue", "han", "este", "esta", "esto", "para", "como", "cada", "todo",
    "toda", "desde", "hasta", "sobre", "entre", "tiene", "tienen", "hace", "hacer",
    "automatico", "automatica", "proceso", "cliente", "empresa", "datos", "sistema",
    "sistemas", "manual", "manuales", "actual", "actualmente", "ningun", "ninguna",
}


def _tokenizar(texto: str) -> set:
    """Extrae palabras significativas (≥3 chars, sin puntuación, sin stopwords).
    El mínimo de 3 deja pasar acrónimos clave del dominio (AFIP, CAE, IVA, CRM...)."""
    import re
    palabras = re.findall(r"[a-záéíóúñ0-9]+", texto.lower())
    return {w for w in palabras if len(w) >= 3 and w not in _STOPWORDS}


def _match_keyword_fallback(req: Dict, servicios: List[Dict]) -> Dict:
    """Fallback determinístico (sin IA) por solapamiento de palabras. Garantiza
    que el análisis funcione aunque no haya ANTHROPIC_API_KEY configurada."""
    texto_req = " ".join(str(req.get(k, "") or "") for k in (
        "nombre_proceso", "trigger_proceso", "pasos_manuales", "sector", "uso_ia"
    ))
    palabras_req = _tokenizar(texto_req)

    mejor, mejor_score = None, 0
    for s in servicios:
        texto_s = f"{s.get('nombre','')} {s.get('categoria','')} {s.get('descripcion','')} {s.get('capacidades','')}"
        palabras_s = _tokenizar(texto_s)
        score = len(palabras_req & palabras_s)
        if score > mejor_score:
            mejor, mejor_score = s, score

    # Umbral mínimo de coincidencia para considerarlo "cubierto".
    if mejor and mejor_score >= 2:
        return {"cubierto": True, "servicio_id": mejor["id"], "confianza": min(60, 30 + mejor_score * 10),
                "justificacion": f"Coincidencia básica por palabras clave con «{mejor['nombre']}» (análisis sin IA; configurá ANTHROPIC_API_KEY para un match más preciso)."}
    return {"cubierto": False, "servicio_id": None, "confianza": 0,
            "justificacion": "Ningún servicio del catálogo coincide claramente (análisis básico sin IA)."}


def match_requerimiento_servicios(req: Dict, servicios: List[Dict]) -> Dict:
    """
    Compara un requerimiento contra el catálogo de servicios y decide si alguno
    lo cubre. Devuelve {cubierto, servicio_id, confianza, justificacion}.
    Si no hay servicios o no hay API key, usa el fallback por keywords.
    """
    if not servicios:
        return {"cubierto": False, "servicio_id": None, "confianza": 0,
                "justificacion": "No hay servicios cargados en el catálogo todavía."}

    if not os.getenv("ANTHROPIC_API_KEY", ""):
        return _match_keyword_fallback(req, servicios)

    servicios_txt = "\n".join(
        f"- ID {s['id']}: {s['nombre']}"
        + (f" [{s['categoria']}]" if s.get("categoria") else "")
        + (f" — {s['descripcion']}" if s.get("descripcion") else "")
        + (f" | Capacidades: {s['capacidades']}" if s.get("capacidades") else "")
        for s in servicios
    )

    prompt = f"""Sos un analista de preventa de una consultora de IA y automatización.
Te paso un REQUERIMIENTO de un cliente y nuestro CATÁLOGO DE SERVICIOS ya construidos.
Decidí si el requerimiento puede cubrirse con ALGUNO de los servicios existentes.

REQUERIMIENTO:
- Cliente: {req.get('nombre_cliente','')}
- Sector: {req.get('sector','')}
- Proceso a automatizar: {req.get('nombre_proceso','')}
- Gatillo: {req.get('trigger_proceso','')}
- Pasos manuales hoy: {req.get('pasos_manuales','')}
- Sistemas/stack: {req.get('sistemas_core','')}
- Uso de IA actual: {req.get('uso_ia','')}

CATÁLOGO DE SERVICIOS:
{servicios_txt}

Reglas:
- Elegí el servicio que mejor cubra el requerimiento SOLO si encaja de verdad.
- Si ninguno encaja bien, marcá cubierto=false (se derivará al área de desarrollo).
- confianza es 0-100 (qué tan seguro estás del match).
- Sé honesto: ante la duda, cubierto=false.

Respondé ÚNICAMENTE con JSON válido, sin texto adicional ni markdown:
{{
  "cubierto": <true|false>,
  "servicio_id": <id del servicio elegido o null>,
  "confianza": <int 0-100>,
  "justificacion": "<1-2 oraciones en español rioplatense explicando por qué>"
}}"""

    res = _call_claude(prompt, max_tokens=600)
    if not res["ok"]:
        # Si la IA falla, intentamos el fallback antes de rendirnos.
        fb = _match_keyword_fallback(req, servicios)
        fb["justificacion"] = f"{fb['justificacion']} (IA no disponible: {res['error']})"
        return fb

    data = res["data"]
    # Validación defensiva del JSON devuelto.
    sid = data.get("servicio_id")
    if data.get("cubierto") and sid is not None:
        ids_validos = {s["id"] for s in servicios}
        if sid not in ids_validos:
            sid = None
            data["cubierto"] = False
    return {
        "cubierto": bool(data.get("cubierto")),
        "servicio_id": sid if data.get("cubierto") else None,
        "confianza": int(data.get("confianza") or 0),
        "justificacion": str(data.get("justificacion") or ""),
    }


# ── 1. Análisis de commits (existente) ────────────────────────────────────────

def analyze_commits(commits: List[Dict], tareas: List[Dict], plan: List[Dict]) -> Dict:
    """
    Devuelve {"task_updates": [...], "plan_updates": [...], "summary": str}
    """
    if not os.getenv("ANTHROPIC_API_KEY", ""):
        return {"task_updates": [], "plan_updates": [],
                "summary": "ANTHROPIC_API_KEY no configurada. Configurala en backend/.env para activar el análisis con IA."}

    tareas_txt = "\n".join(
        f"- ID {t['id']}: [{t['status']}] {t['titulo']}"
        + (f" — {t['descripcion']}" if t.get("descripcion") else "")
        for t in tareas
    ) or "Sin tareas"

    plan_txt = "\n".join(
        f"- ID {p['id']}: [{'✓' if p['completado'] else '○'}] {p['titulo']}"
        for p in plan
    ) or "Sin puntos de acción"

    commits_txt = "\n".join(
        f"- {c['sha']} ({c['date']}) {c['author']}: {c['message']}"
        for c in commits
    ) or "Sin commits"

    prompt = f"""Sos un asistente de gestión de proyectos. Analizá los commits de GitHub y determiná qué tareas y puntos del plan de acción se deben actualizar.

TAREAS ACTUALES:
{tareas_txt}

PLAN DE ACCIÓN:
{plan_txt}

COMMITS RECIENTES:
{commits_txt}

Reglas:
- Si un commit implica que se completó una tarea, actualizá su estado a "completada"
- Si un commit inicia trabajo en una tarea pendiente, pasala a "en_progreso"
- Si un commit indica que un punto del plan fue alcanzado, marcalo como completado (true)
- Solo actualizá cuando haya evidencia clara en los mensajes de commit
- No retrocedas el estado de tareas ya completadas
- Si no hay cambios claros, devolvé arrays vacíos

Respondé ÚNICAMENTE con JSON válido, sin texto adicional ni markdown:
{{
  "task_updates": [{{"id": <int>, "status": "<pendiente|en_progreso|revision|completada|bloqueada>", "reason": "<razón breve>"}}],
  "plan_updates": [{{"id": <int>, "completado": <true|false>, "reason": "<razón breve>"}}],
  "summary": "<resumen en español, máx 2 oraciones>"
}}"""

    res = _call_claude(prompt, max_tokens=1500)
    if not res["ok"]:
        return {"task_updates": [], "plan_updates": [], "summary": res["error"]}
    return res["data"]


# ── 2. Generar plan de acción ─────────────────────────────────────────────────

def generate_plan(nombre: str, cliente: str, descripcion: Optional[str],
                  tareas_existentes: List[Dict]) -> Dict:
    """
    Genera puntos del plan de acción a partir del contexto del proyecto.
    Devuelve {"plan": [{"titulo": str, "descripcion": str}], "summary": str}.
    """
    tareas_txt = "\n".join(
        f"- {t['titulo']}" + (f": {t['descripcion']}" if t.get("descripcion") else "")
        for t in tareas_existentes
    ) or "(sin tareas todavía)"

    prompt = f"""Sos un asistente de gestión de proyectos para una consultora de IA y automatización.
Generá un PLAN DE ACCIÓN realista y bien estructurado para este proyecto.

PROYECTO: {nombre}
CLIENTE: {cliente}
DESCRIPCIÓN: {descripcion or "(sin descripción)"}

TAREAS YA CREADAS (referencia, no las repitas):
{tareas_txt}

El plan de acción debe tener entre 5 y 8 hitos/entregables, ordenados cronológicamente,
desde el relevamiento hasta la entrega final. Cada punto representa una etapa o entregable
mayor del proyecto, NO una tarea granular. Usá lenguaje claro en español rioplatense.

Respondé ÚNICAMENTE con JSON válido:
{{
  "plan": [
    {{"titulo": "<hito en 5-10 palabras>", "descripcion": "<qué incluye este hito, 1 oración>"}}
  ],
  "summary": "<resumen breve del enfoque elegido, 1-2 oraciones>"
}}"""

    res = _call_claude(prompt, max_tokens=2000)
    if not res["ok"]:
        return {"plan": [], "summary": res["error"]}
    return res["data"]


# ── 3. Generar tareas a partir del plan ───────────────────────────────────────

def generate_tasks(nombre: str, cliente: str, descripcion: Optional[str],
                   plan: List[Dict], tareas_existentes: List[Dict]) -> Dict:
    """
    Genera tareas granulares desde el plan + descripción del proyecto.
    Devuelve {"tareas": [{"titulo": str, "descripcion": str, "prioridad": str, "minutos_estimados": int}], "summary": str}.
    """
    plan_txt = "\n".join(f"- {p['titulo']}" + (f": {p.get('descripcion','')}" if p.get('descripcion') else "")
                         for p in plan) or "(sin plan definido)"

    existentes_txt = "\n".join(f"- {t['titulo']}" for t in tareas_existentes) or "(sin tareas previas)"

    prompt = f"""Sos un asistente de gestión de proyectos para una consultora de IA y automatización.
Generá las TAREAS GRANULARES necesarias para ejecutar este proyecto.

PROYECTO: {nombre}
CLIENTE: {cliente}
DESCRIPCIÓN: {descripcion or "(sin descripción)"}

PLAN DE ACCIÓN:
{plan_txt}

TAREAS YA EXISTENTES (no las repitas, generá las que falten):
{existentes_txt}

Generá entre 6 y 12 tareas concretas, cada una con título corto, descripción de 1 oración,
prioridad (baja|media|alta|urgente) y estimación realista en minutos.
Las tareas deben ser unidades de trabajo de 30 min a 8 horas.

Respondé ÚNICAMENTE con JSON válido:
{{
  "tareas": [
    {{
      "titulo": "<acción concreta, max 60 chars>",
      "descripcion": "<qué hay que hacer, 1 oración>",
      "prioridad": "baja|media|alta|urgente",
      "minutos_estimados": <int>
    }}
  ],
  "summary": "<resumen breve del enfoque, 1 oración>"
}}"""

    res = _call_claude(prompt, max_tokens=3000)
    if not res["ok"]:
        return {"tareas": [], "summary": res["error"]}
    return res["data"]


# ── 4. Analizar documento y dividir en plan + tareas ──────────────────────────

def analyze_document(contenido: str, nombre: str, cliente: str) -> Dict:
    """
    Recibe el contenido textual de un documento (relevamiento, propuesta, brief)
    y lo divide automáticamente en plan de acción + tareas.
    """
    # Truncar el documento para que entre en el contexto sin gastar demasiado
    contenido_corto = contenido.strip()[:12000]

    prompt = f"""Sos un asistente de gestión de proyectos para una consultora de IA y automatización.
El usuario subió un documento (relevamiento, propuesta, brief, etc.) sobre el proyecto.
Analizá el contenido y dividilo en (a) plan de acción de alto nivel y (b) tareas granulares ejecutables.

PROYECTO: {nombre}
CLIENTE: {cliente}

CONTENIDO DEL DOCUMENTO:
\"\"\"
{contenido_corto}
\"\"\"

Reglas:
- El plan de acción son hitos/entregables (5 a 8 puntos), ordenados cronológicamente.
- Las tareas son unidades de trabajo concretas (6 a 14 ítems), de 30 min a 8 horas cada una.
- Usá lenguaje claro en español rioplatense.
- Si el documento es ambiguo, completá con criterio profesional.

Respondé ÚNICAMENTE con JSON válido:
{{
  "plan": [
    {{"titulo": "<hito>", "descripcion": "<detalle 1 oración>"}}
  ],
  "tareas": [
    {{
      "titulo": "<acción concreta>",
      "descripcion": "<qué hay que hacer>",
      "prioridad": "baja|media|alta|urgente",
      "minutos_estimados": <int>
    }}
  ],
  "summary": "<resumen del proyecto extraído del documento, 2-3 oraciones>"
}}"""

    res = _call_claude(prompt, max_tokens=4000)
    if not res["ok"]:
        return {"plan": [], "tareas": [], "summary": res["error"]}
    return res["data"]
