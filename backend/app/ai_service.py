import os
import json
import httpx
from typing import List, Dict

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"


def analyze_commits(
    commits: List[Dict],
    tareas: List[Dict],
    plan: List[Dict],
) -> Dict:
    """
    Calls Claude to infer which tasks/plan-points should be updated based on commit messages.

    Returns:
        {
            "task_updates": [{"id": int, "status": str, "reason": str}],
            "plan_updates": [{"id": int, "completado": bool, "reason": str}],
            "summary": str
        }
    """
    if not ANTHROPIC_API_KEY:
        return {
            "task_updates": [],
            "plan_updates": [],
            "summary": "ANTHROPIC_API_KEY no configurada. Configurala en backend/.env para activar el análisis con IA.",
        }

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

    prompt = f"""Sos un asistente de gestión de proyectos. Analizá los commits de GitHub y determiná qué tareas y puntos del plan de acción se deben actualizar automáticamente.

TAREAS ACTUALES:
{tareas_txt}

PLAN DE ACCIÓN:
{plan_txt}

COMMITS RECIENTES:
{commits_txt}

Reglas:
- Si un commit implica que se completó una tarea, actualizá su estado a "completada"
- Si un commit inicia trabajo en una tarea pendiente, actualizá a "en_progreso"
- Si un commit indica que un punto del plan fue alcanzado, marcalo como completado (true)
- Solo actualizá cuando haya evidencia clara en los mensajes de commit
- No retrocedas el estado de tareas ya completadas
- Si no hay cambios claros, devolvé arrays vacíos

Respondé ÚNICAMENTE con JSON válido, sin texto adicional ni markdown:
{{
  "task_updates": [
    {{"id": <int>, "status": "<pendiente|en_progreso|revision|completada|bloqueada>", "reason": "<razón breve en español>"}}
  ],
  "plan_updates": [
    {{"id": <int>, "completado": <true|false>, "reason": "<razón breve en español>"}}
  ],
  "summary": "<resumen en español de los cambios detectados, máximo 2 oraciones>"
}}"""

    try:
        resp = httpx.post(
            ANTHROPIC_URL,
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        resp.raise_for_status()
        raw = resp.json()["content"][0]["text"].strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except json.JSONDecodeError as e:
        return {"task_updates": [], "plan_updates": [], "summary": f"Error al parsear respuesta IA: {e}"}
    except httpx.HTTPStatusError as e:
        return {"task_updates": [], "plan_updates": [], "summary": f"Error API Anthropic {e.response.status_code}: {e.response.text[:200]}"}
    except Exception as e:
        return {"task_updates": [], "plan_updates": [], "summary": f"Error IA: {e}"}
