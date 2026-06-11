"""
Servicio de email con templates HTML on-brand (Optimizar).
Usa smtplib nativo — sin dependencias extra.
Configurar via variables de entorno en .env.
"""
import smtplib
import ssl
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# ── Config SMTP ───────────────────────────────────────────────────────────────

SMTP_HOST     = os.getenv("SMTP_HOST", "")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER     = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_NAME     = os.getenv("FROM_NAME", "Optimizar IA")
FROM_EMAIL    = os.getenv("FROM_EMAIL", SMTP_USER)
APP_URL       = os.getenv("APP_URL", "http://localhost:5173")
NOTIFICATIONS_ENABLED = os.getenv("NOTIFICATIONS_ENABLED", "false").lower() == "true"

# ── HTML Base Template ────────────────────────────────────────────────────────

def _base_html(titulo: str, subtitulo: str, cuerpo: str, cta_url: str = "", cta_label: str = "") -> str:
    cta_block = ""
    if cta_url and cta_label:
        cta_block = f"""
        <tr>
          <td style="padding: 0 40px 32px;">
            <a href="{cta_url}"
               style="display:inline-block; background:#6366F1; color:#fff;
                      text-decoration:none; font-size:13px; font-weight:600;
                      letter-spacing:-0.01em; padding:12px 28px;
                      border-radius:100px;">
              {cta_label}
            </a>
          </td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{titulo}</title>
</head>
<body style="margin:0;padding:0;background:#F8FAFC;font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#F8FAFC;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

          <!-- Header -->
          <tr>
            <td style="background:#0F172A;border-radius:20px 20px 0 0;padding:28px 40px;
                       display:block;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td>
                    <span style="font-size:22px;font-weight:800;color:#fff;
                                 letter-spacing:-0.04em;line-height:1;">
                      Optimizar
                      <span style="display:inline-block;width:8px;height:8px;
                                   background:#6366F1;border-radius:2px;
                                   vertical-align:middle;margin-left:2px;
                                   margin-bottom:3px;"></span>
                    </span>
                  </td>
                  <td align="right">
                    <span style="font-size:10px;color:#64748B;letter-spacing:0.18em;
                                 text-transform:uppercase;font-weight:600;">
                      Automatización · IA
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Accent bar -->
          <tr>
            <td style="background:linear-gradient(90deg,#6366F1,#818CF8);
                       height:3px;"></td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="background:#fff;padding:36px 40px 24px;">
              <p style="margin:0 0 4px;font-size:11px;font-weight:600;
                        color:#6366F1;letter-spacing:0.2em;text-transform:uppercase;">
                Notificación
              </p>
              <h1 style="margin:0 0 6px;font-size:26px;font-weight:800;color:#0F172A;
                         letter-spacing:-0.04em;line-height:1.1;">
                {titulo}
              </h1>
              <p style="margin:0 0 28px;font-size:15px;color:#64748B;font-weight:300;
                        line-height:1.6;">
                {subtitulo}
              </p>
              <div style="border-top:1px solid #E2E8F0;padding-top:24px;">
                {cuerpo}
              </div>
            </td>
          </tr>

          <!-- CTA -->
          {f'<tr><td style="background:#fff;padding:0 40px 32px;">{_cta_inner(cta_url, cta_label)}</td></tr>' if cta_url else ''}

          <!-- Footer -->
          <tr>
            <td style="background:#F1F5F9;border-radius:0 0 20px 20px;
                       padding:20px 40px;border-top:1px solid #E2E8F0;">
              <p style="margin:0;font-size:11px;color:#94A3B8;line-height:1.6;">
                Este es un mensaje automático de <strong>Optimizar IA</strong>.
                No respondas este correo directamente.<br/>
                <a href="{APP_URL}" style="color:#6366F1;text-decoration:none;">
                  Ir a la plataforma
                </a>
                &nbsp;·&nbsp;
                {datetime.now().strftime("%d/%m/%Y")}
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def _cta_inner(url: str, label: str) -> str:
    return f"""<a href="{url}"
       style="display:inline-block; background:#6366F1; color:#fff;
              text-decoration:none; font-size:13px; font-weight:600;
              letter-spacing:-0.01em; padding:12px 28px;
              border-radius:100px;">
      {label}
    </a>"""


def _campo(label: str, valor: str) -> str:
    """Fila de dato dentro del cuerpo del email."""
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:12px;">
      <tr>
        <td style="background:#F8FAFC;border-radius:12px;padding:12px 16px;
                   border:1px solid #E2E8F0;">
          <span style="display:block;font-size:10px;font-weight:600;color:#94A3B8;
                       text-transform:uppercase;letter-spacing:0.14em;margin-bottom:3px;">
            {label}
          </span>
          <span style="font-size:14px;color:#0F172A;font-weight:500;">{valor}</span>
        </td>
      </tr>
    </table>"""


def _badge(texto: str, color: str = "#6366F1") -> str:
    return f"""<span style="display:inline-block;background:{color}20;color:{color};
                  font-size:11px;font-weight:600;padding:3px 10px;
                  border-radius:100px;letter-spacing:-0.01em;">{texto}</span>"""


# ── Colores por estado ────────────────────────────────────────────────────────

STATUS_COLOR = {
    "pendiente":   "#64748B",
    "en_progreso": "#6366F1",
    "revision":    "#B45309",
    "completada":  "#059669",
    "bloqueada":   "#DC2626",
}
STATUS_LABEL = {
    "pendiente":   "Pendiente",
    "en_progreso": "En progreso",
    "revision":    "En revisión",
    "completada":  "Completada",
    "bloqueada":   "Bloqueada",
}
PRIO_COLOR = {
    "baja":    "#94A3B8",
    "media":   "#0F172A",
    "alta":    "#B45309",
    "urgente": "#DC2626",
}
PRIO_LABEL = {"baja": "Baja", "media": "Media", "alta": "Alta", "urgente": "Urgente"}


# ── Generadores de templates ──────────────────────────────────────────────────

def template_tarea_asignada(tarea, proyecto_nombre: str, asignado_nombre: str) -> tuple[str, str]:
    """Retorna (asunto, html)."""
    tarea_url = f"{APP_URL}/proyecto/{tarea.proyecto_id}"
    prioridad = tarea.prioridad.value if hasattr(tarea.prioridad, 'value') else str(tarea.prioridad)
    status    = tarea.status.value if hasattr(tarea.status, 'value') else str(tarea.status)

    cuerpo = (
        _campo("Proyecto", proyecto_nombre) +
        _campo("Tarea", tarea.titulo) +
        (f"<p style='font-size:13px;color:#64748B;line-height:1.6;margin:0 0 16px;'>{tarea.descripcion}</p>"
         if tarea.descripcion else "") +
        f"<div style='margin-bottom:16px;'>{_badge(PRIO_LABEL.get(prioridad, prioridad), PRIO_COLOR.get(prioridad, '#64748B'))}</div>" +
        (f"<p style='font-size:12px;color:#94A3B8;margin:0;'>Fecha estimada: "
         f"<strong style='color:#0F172A;'>{tarea.fecha_fin_estimada.strftime('%d/%m/%Y')}</strong></p>"
         if tarea.fecha_fin_estimada else "")
    )

    asunto = f"Nueva tarea asignada: {tarea.titulo}"
    html = _base_html(
        titulo=f"Te asignaron una tarea.",
        subtitulo=f"Hola {asignado_nombre}, tenés una nueva tarea en el proyecto {proyecto_nombre}.",
        cuerpo=cuerpo,
        cta_url=tarea_url,
        cta_label="Ver tarea",
    )
    return asunto, html


def template_cambio_estado(tarea, proyecto_nombre: str, destinatario_nombre: str,
                            estado_anterior: str, estado_nuevo: str) -> tuple[str, str]:
    tarea_url = f"{APP_URL}/proyecto/{tarea.proyecto_id}"
    color_nuevo = STATUS_COLOR.get(estado_nuevo, "#6366F1")

    cuerpo = (
        _campo("Proyecto", proyecto_nombre) +
        _campo("Tarea", tarea.titulo) +
        f"""<table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:12px;">
          <tr>
            <td style="background:#F8FAFC;border-radius:12px;padding:12px 16px;border:1px solid #E2E8F0;">
              <span style="display:block;font-size:10px;font-weight:600;color:#94A3B8;
                           text-transform:uppercase;letter-spacing:0.14em;margin-bottom:8px;">
                Cambio de estado
              </span>
              <span style="margin-right:8px;">{_badge(STATUS_LABEL.get(estado_anterior, estado_anterior), STATUS_COLOR.get(estado_anterior, '#64748B'))}</span>
              <span style="font-size:12px;color:#94A3B8;margin-right:8px;">→</span>
              {_badge(STATUS_LABEL.get(estado_nuevo, estado_nuevo), color_nuevo)}
            </td>
          </tr>
        </table>"""
    )

    asunto = f"Tarea actualizada: {tarea.titulo} → {STATUS_LABEL.get(estado_nuevo, estado_nuevo)}"
    html = _base_html(
        titulo=f"Estado de tarea actualizado.",
        subtitulo=f"Hola {destinatario_nombre}, el estado de una tarea cambió.",
        cuerpo=cuerpo,
        cta_url=tarea_url,
        cta_label="Ver tarea",
    )
    return asunto, html


def template_reasignacion(tarea, proyecto_nombre: str, nuevo_asignado_nombre: str,
                           anterior_nombre: Optional[str]) -> tuple[str, str]:
    tarea_url = f"{APP_URL}/proyecto/{tarea.proyecto_id}"
    prioridad = tarea.prioridad.value if hasattr(tarea.prioridad, 'value') else str(tarea.prioridad)

    cuerpo = (
        _campo("Proyecto", proyecto_nombre) +
        _campo("Tarea", tarea.titulo) +
        (f"<p style='font-size:13px;color:#64748B;line-height:1.6;margin:0 0 12px;'>{tarea.descripcion}</p>"
         if tarea.descripcion else "") +
        (f"<p style='font-size:12px;color:#94A3B8;margin:0 0 4px;'>Asignado anteriormente a: "
         f"<strong style='color:#0F172A;'>{anterior_nombre}</strong></p>"
         if anterior_nombre else "") +
        f"<div style='margin-top:8px;'>{_badge(PRIO_LABEL.get(prioridad, prioridad), PRIO_COLOR.get(prioridad, '#64748B'))}</div>"
    )

    asunto = f"Tarea reasignada a vos: {tarea.titulo}"
    html = _base_html(
        titulo="Te reasignaron una tarea.",
        subtitulo=f"Hola {nuevo_asignado_nombre}, la tarea fue asignada a tu nombre.",
        cuerpo=cuerpo,
        cta_url=tarea_url,
        cta_label="Ver tarea",
    )
    return asunto, html


def template_detalles_actualizados(tarea, proyecto_nombre: str, destinatario_nombre: str,
                                    cambios: list[str]) -> tuple[str, str]:
    tarea_url = f"{APP_URL}/proyecto/{tarea.proyecto_id}"

    cambios_html = "".join([
        f"<li style='font-size:13px;color:#0F172A;margin-bottom:4px;'>{c}</li>"
        for c in cambios
    ])
    cuerpo = (
        _campo("Proyecto", proyecto_nombre) +
        _campo("Tarea", tarea.titulo) +
        f"""<div style="background:#F8FAFC;border-radius:12px;padding:12px 16px;
                        border:1px solid #E2E8F0;">
          <span style="display:block;font-size:10px;font-weight:600;color:#94A3B8;
                       text-transform:uppercase;letter-spacing:0.14em;margin-bottom:8px;">
            Cambios realizados
          </span>
          <ul style="margin:0;padding-left:18px;">{cambios_html}</ul>
        </div>"""
    )

    asunto = f"Tarea modificada: {tarea.titulo}"
    html = _base_html(
        titulo="Una tarea fue modificada.",
        subtitulo=f"Hola {destinatario_nombre}, se actualizaron los detalles de una tarea asignada a vos.",
        cuerpo=cuerpo,
        cta_url=tarea_url,
        cta_label="Ver tarea",
    )
    return asunto, html


def template_tarea_completada(tarea, proyecto_nombre: str, destinatario_nombre: str,
                               completado_por: str) -> tuple[str, str]:
    tarea_url = f"{APP_URL}/proyecto/{tarea.proyecto_id}"
    minutos = sum(r.minutos for r in tarea.registros) if tarea.registros else 0
    horas = f"{minutos // 60}h {minutos % 60}m" if minutos else "—"

    cuerpo = (
        _campo("Proyecto", proyecto_nombre) +
        _campo("Tarea", tarea.titulo) +
        _campo("Completada por", completado_por) +
        _campo("Tiempo total registrado", horas) +
        f"<div style='margin-top:4px;'>{_badge('Completada', '#059669')}</div>"
    )

    asunto = f"Tarea completada: {tarea.titulo}"
    html = _base_html(
        titulo="Tarea completada.",
        subtitulo=f"Hola {destinatario_nombre}, la tarea fue marcada como completada.",
        cuerpo=cuerpo,
        cta_url=tarea_url,
        cta_label="Ver proyecto",
    )
    return asunto, html


# ── Envío SMTP ────────────────────────────────────────────────────────────────

def _send_smtp(to_email: str, asunto: str, html: str) -> Optional[str]:
    """Envía el email. Retorna None si OK, mensaje de error si falla."""
    if not NOTIFICATIONS_ENABLED:
        logger.info(f"[EMAIL DISABLED] Para: {to_email} | Asunto: {asunto}")
        return None
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASSWORD:
        logger.warning("SMTP no configurado. Revisar SMTP_HOST, SMTP_USER, SMTP_PASSWORD en .env")
        return "SMTP no configurado"

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = asunto
        msg["From"]    = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg["To"]      = to_email
        msg.attach(MIMEText(html, "html", "utf-8"))

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())

        logger.info(f"Email enviado → {to_email} | {asunto}")
        return None

    except Exception as e:
        logger.error(f"Error enviando email a {to_email}: {e}")
        return str(e)


# ── Entry point principal ────────────────────────────────────────────────────

# ── Avisos del Equipo de Venta y Prospección ──────────────────────────────────

# Destinatarios de los reportes/alertas del funnel (configurable por env).
FUNNEL_NOTIFY_EMAILS = [
    e.strip() for e in os.getenv(
        "FUNNEL_NOTIFY_EMAILS",
        "rodriguezfederico765@gmail.com,optimizar.ai@gmail.com",
    ).split(",") if e.strip()
]


def enviar_aviso_funnel(asunto: str, titulo: str, subtitulo: str, cuerpo_html: str,
                        prioridad: str = "info") -> dict:
    """Envía un reporte/alerta del funnel a TODOS los correos configurados.
    Retorna {email: None|error} por destinatario. No persiste en Notificacion
    (esa tabla es task-centric); el chat de la plataforma es el registro del funnel."""
    badge = _badge("ALERTA", "#DC2626") if prioridad == "alerta" else _badge("Reporte", "#6366F1")
    cuerpo = f"<div style='margin-bottom:16px;'>{badge}</div>{cuerpo_html}"
    html = _base_html(titulo=titulo, subtitulo=subtitulo or "", cuerpo=cuerpo,
                      cta_url=APP_URL, cta_label="Ir a la plataforma")
    resultados = {}
    for email in FUNNEL_NOTIFY_EMAILS:
        resultados[email] = _send_smtp(email, asunto, html)
    return resultados


def registrar_y_enviar(
    db: Session,
    tipo,
    destinatario_email: str,
    asunto: str,
    html: str,
    tarea_id: Optional[int] = None,
    destinatario_id: Optional[int] = None,
) -> None:
    """Guarda la notificación en BD y envía el email. Llama desde BackgroundTasks."""
    from app.models import Notificacion
    error = _send_smtp(destinatario_email, asunto, html)
    notif = Notificacion(
        tipo=tipo,
        destinatario_id=destinatario_id,
        destinatario_email=destinatario_email,
        tarea_id=tarea_id,
        asunto=asunto,
        cuerpo_html=html,
        enviado=(error is None),
        error=error,
    )
    db.add(notif)
    db.commit()
