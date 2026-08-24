"""Trae el diagnóstico que el prospecto completó antes de escribir por WhatsApp.

El CTA del diagnóstico abre WhatsApp con el mensaje ya escrito y el código adentro:
"Hola, leí mi diagnóstico y quiero avanzar. Código: zkRo7hvt2Y3R". Con ese código
Gero sabe con quién habla antes de decir la primera palabra.

La tabla `diagnosticos` la escribe la app del diagnóstico, que es otro servicio.
Comparten base de datos, así que la leemos con SQL directo en vez de declarar un
modelo de SQLAlchemy: declararlo metería esta tabla en el `create_all` de la
plataforma, y dos servicios gestionando el mismo esquema es una fuente de
problemas silenciosos. Acá solo leemos, nunca escribimos.
"""
import json
import logging
import os
import re
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import GeroMensaje

logger = logging.getLogger(__name__)

# De acá sale el link que Gero le pasa al prospecto para leer su diagnóstico.
DIAGNOSTICO_URL = os.getenv("DIAGNOSTICO_URL", "https://diagnostico.optimizar-ia.com").rstrip("/")

# El token es `secrets.token_urlsafe(9)`: 12 caracteres de [A-Za-z0-9_-].
# Aceptamos "Código" y "Codigo" porque el acento se pierde en algunos teclados.
_CODIGO = re.compile(r"[Cc][óo]digo\s*:?\s*([A-Za-z0-9_\-]{10,16})")


def token_en(texto: str) -> Optional[str]:
    """Extrae el código de diagnóstico de un mensaje, si lo tiene."""
    if not texto:
        return None
    m = _CODIGO.search(texto)
    return m.group(1) if m else None


def token_de_conversacion(db: Session, conversacion_id: int) -> Optional[str]:
    """Busca el código en todo el historial de la conversación.

    Se escanea el historial y no solo el último mensaje a propósito: el código
    llega en el primer mensaje, pero Gero tiene que seguir sabiendo quién es la
    persona en el turno veinte. Y si alguien lo pega más tarde, también sirve.
    """
    filas = (db.query(GeroMensaje.contenido)
               .filter(GeroMensaje.conversacion_id == conversacion_id,
                       GeroMensaje.rol == "user")
               .order_by(GeroMensaje.created_at.asc())
               .limit(60)
               .all())
    for (contenido,) in filas:
        t = token_en(contenido or "")
        if t:
            return t
    return None


def _como_dict(valor) -> dict:
    """El contenido puede venir como dict (JSON de Postgres) o como string."""
    if isinstance(valor, dict):
        return valor
    if isinstance(valor, str) and valor.strip():
        try:
            return json.loads(valor)
        except json.JSONDecodeError:
            return {}
    return {}


def _redactar(fila) -> str:
    """Arma el bloque de contexto que se le inyecta a Gero en el system prompt."""
    contenido = _como_dict(fila.contenido)
    respuestas = _como_dict(fila.respuestas)
    motivos = fila.motivos if isinstance(fila.motivos, list) else _como_dict(fila.motivos) or []

    partes = ["# ESTA PERSONA YA COMPLETÓ EL DIAGNÓSTICO",
              "",
              "No le pidas datos que ya te dio. Arrancá desde acá."]

    quien = " · ".join(x for x in (fila.nombre, fila.email, fila.telefono) if x)
    if quien:
        partes.append(f"\nQuién es: {quien}")

    if respuestas:
        crudas = ", ".join(
            f"{k}: {', '.join(v) if isinstance(v, list) else v}"
            for k, v in respuestas.items() if v
        )
        partes.append(f"\nLo que respondió en el formulario:\n{crudas}")

    link = f"{DIAGNOSTICO_URL}/d/{fila.token}"
    if (fila.variante or "").lower() == "b":
        # La variante B entrega el informe por WhatsApp: esta persona vino a
        # buscarlo, no a charlar. Si Gero no le pasa el link, esa rama del
        # test A/B queda sin entregar.
        partes.append(
            f"\nVINO A RECIBIR SU DIAGNOSTICO POR ACA. Lo primero que tenes que hacer "
            f"es pasarle el link, antes de cualquier otra cosa: {link}"
        )
    else:
        partes.append(f"\nSi te lo pide de nuevo o lo perdio, esta en: {link}")

    if fila.estado != "listo":
        partes.append(f"\n⚠️ El diagnóstico todavía se está generando (estado: {fila.estado}). "
                      "Si pregunta por él, decile que le llega en un par de minutos.")
    elif contenido:
        partes.append("\nEL DIAGNÓSTICO QUE YA LEYÓ (podés citarlo, lo tiene fresco):")
        if contenido.get("titular"):
            partes.append(f"  Titular: {contenido['titular']}")
        if contenido.get("resumen"):
            partes.append(f"  Resumen: {contenido['resumen']}")
        for i, c in enumerate(contenido.get("cuellos") or [], 1):
            partes.append(f"  Cuello {i}: {c.get('titulo','')} — {c.get('descripcion','')} "
                          f"(impacto: {c.get('impacto','')})")
        rec = contenido.get("recomendacion") or {}
        if rec:
            partes.append(f"  Le recomendamos: {rec.get('titulo','')} — {rec.get('descripcion','')} "
                          f"(plazo estimado: {rec.get('plazo','')})")
        qw = contenido.get("quick_win") or {}
        if qw:
            partes.append(f"  Quick win que le regalamos: {qw.get('titulo','')}")

    # La calificación es interna: define cuánto empujás, nunca se menciona.
    tier = (fila.tier or "amarillo").lower()
    guias = {
        "verde": ("CALIENTE. Encaja con lo que hacemos y tiene urgencia. Tu objetivo en esta "
                  "charla es que agende. Ofrecele la reunión temprano, sin dar mil vueltas."),
        "amarillo": ("TIBIO. Encaja pero sin urgencia, o no es quien decide. No lo apures: "
                     "resolvele las dudas primero y ofrecé la reunión cuando se entusiasme."),
        "rojo": ("NO CALIFICA. Atendelo igual y con buena onda —el diagnóstico ya es suyo—, "
                 "pero NO insistas con agendar. Si pregunta, contestá bien y dejá la puerta "
                 "abierta. Nada de vender."),
    }
    partes.append(f"\n# CALIFICACIÓN INTERNA — NO SE LA MENCIONES NUNCA\n{guias.get(tier, guias['amarillo'])}")
    if motivos:
        partes.append("Motivos: " + "; ".join(str(m) for m in motivos))

    if any("xclusi" in str(m) for m in motivos):
        partes.append("\n🚫 IMPORTANTE: esta persona cae en una exclusión contractual "
                      "(estudio contable en La Pampa, por el acuerdo con Larrañaga y Asociados). "
                      "No le ofrezcas servicios ni reunión. Si insiste, pasalo a un humano "
                      "con `handoff_humano`.")

    return "\n".join(partes)


def contexto(db: Session, token: str) -> Optional[str]:
    """Devuelve el bloque de contexto del diagnóstico, o None si no existe.

    Nunca levanta: si la tabla no está (por ejemplo en un entorno donde solo corre
    la plataforma), Gero sigue funcionando como siempre.
    """
    if not token:
        return None
    try:
        fila = db.execute(text("""
            SELECT token, variante, nombre, email, telefono, respuestas,
                   contenido, tier, motivos, estado
              FROM diagnosticos
             WHERE token = :token
             LIMIT 1
        """), {"token": token}).mappings().first()
    except Exception as e:  # tabla ausente, permisos, lo que sea
        logger.warning("[gero] no se pudo leer el diagnóstico %s: %s", token, e)
        return None

    if not fila:
        logger.info("[gero] código %s sin diagnóstico asociado.", token)
        return None

    class _F:  # acceso por atributo, más legible en `_redactar`
        def __init__(self, m): self.__dict__.update(m)

    return _redactar(_F(dict(fila)))
