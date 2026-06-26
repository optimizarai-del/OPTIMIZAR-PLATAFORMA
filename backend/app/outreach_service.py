"""
Servicio de outreach del Equipo de Venta y Prospección — ENVÍO y ESCUCHA en código.
Reemplaza los workflows de n8n: el backend manda los correos ya escritos por los agentes
y lee las respuestas del inbox, sin dependencias externas.

- ENVÍO  : SMTP de Hostinger (mismas vars SMTP_* que ya usa email_service).
- ESCUCHA: IMAP del mismo buzón (imap-tools).

Texto plano a propósito: los correos en frío en plain-text tienen mejor deliverability
que el HTML cargado (parecen escritos por una persona, no por marketing).
"""
import os
import ssl
import time
import smtplib
import logging
from email.mime.text import MIMEText
from email.utils import formataddr

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Contacto

logger = logging.getLogger(__name__)

# ── Config (reutiliza SMTP_* de email_service; agrega IMAP_* y límites de outreach) ──
SMTP_HOST     = os.getenv("SMTP_HOST", "smtp.hostinger.com")
SMTP_PORT     = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER     = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

OUTREACH_ENABLED      = os.getenv("OUTREACH_ENABLED", "false").lower() == "true"
OUTREACH_FROM_NAME    = os.getenv("OUTREACH_FROM_NAME", "OPTIMIZAR")
OUTREACH_FROM_EMAIL   = os.getenv("OUTREACH_FROM_EMAIL", SMTP_USER)
OUTREACH_DAILY_CAP    = int(os.getenv("OUTREACH_DAILY_CAP", "30"))      # tope por corrida (warm-up)
OUTREACH_THROTTLE_SEC = int(os.getenv("OUTREACH_THROTTLE_SEC", "90"))   # espera entre envíos

IMAP_HOST = os.getenv("IMAP_HOST", "imap.hostinger.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))


# ── ENVÍO ─────────────────────────────────────────────────────────────────────

def _enviar_uno(to_email: str, asunto: str, cuerpo: str):
    """Envía un correo en texto plano por SMTP. Retorna None si OK, o el error."""
    if not (SMTP_HOST and SMTP_USER and SMTP_PASSWORD):
        return "SMTP no configurado (SMTP_HOST/USER/PASSWORD)"
    try:
        msg = MIMEText(cuerpo or "", "plain", "utf-8")
        msg["Subject"] = asunto or ""
        msg["From"] = formataddr((OUTREACH_FROM_NAME, OUTREACH_FROM_EMAIL))
        msg["To"] = to_email

        context = ssl.create_default_context()
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as s:
                s.login(SMTP_USER, SMTP_PASSWORD)
                s.sendmail(OUTREACH_FROM_EMAIL, to_email, msg.as_string())
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
                s.ehlo(); s.starttls(context=context); s.login(SMTP_USER, SMTP_PASSWORD)
                s.sendmail(OUTREACH_FROM_EMAIL, to_email, msg.as_string())
        return None
    except Exception as e:
        return str(e)


def enviar_pendientes(db: Session = None) -> int:
    """Manda el primer contacto a los CONTACTOS con estado='escrito'. Al enviar, el contacto
    queda 'contactado' (sigue en la base de Contactos, NO sube al pipeline — solo sube si
    responde). Respeta el tope diario y el throttling de warm-up. Devuelve cuántos envió."""
    propio = db is None
    db = db or SessionLocal()
    enviados = 0
    try:
        # Selección + CLAIM atómico: marcamos 'enviando' con commit ANTES de enviar para que
        # una corrida manual y el cron no tomen el mismo lote → sin doble envío.
        q = (db.query(Contacto)
               .filter(Contacto.estado == "escrito",
                       Contacto.email.isnot(None),
                       Contacto.mensaje_cuerpo.isnot(None))
               .order_by(Contacto.created_at)
               .limit(OUTREACH_DAILY_CAP))
        try:
            pendientes = q.with_for_update(skip_locked=True).all()
        except Exception:
            pendientes = q.all()          # motor sin FOR UPDATE: seguimos igual
        for c in pendientes:
            c.estado = "enviando"
        db.commit()                        # claim confirmado

        total = len(pendientes)
        for i, c in enumerate(pendientes):
            err = _enviar_uno(c.email, c.mensaje_asunto, c.mensaje_cuerpo)
            if err is None:
                c.estado = "contactado"     # contactado sin respuesta — queda en Contactos
                db.commit()
                enviados += 1
                logger.info(f"[outreach] enviado a {c.email} ({c.empresa})")
            else:
                c.estado = "escrito"        # liberar para reintentar
                db.commit()
                logger.error(f"[outreach] fallo enviando a {c.email}: {err}")
            # throttling de warm-up entre envíos (no después del último)
            if i < total - 1 and OUTREACH_THROTTLE_SEC > 0:
                time.sleep(OUTREACH_THROTTLE_SEC)
        if total:
            logger.info(f"[outreach] corrida de envío: {enviados}/{total} enviados.")
        return enviados
    finally:
        if propio:
            db.close()


# ── ESCUCHA ───────────────────────────────────────────────────────────────────

def revisar_inbox(db: Session = None) -> int:
    """Lee respuestas nuevas (no leídas) del inbox por IMAP, matchea el CONTACTO por email
    del remitente, lo marca 'respondido' y lo PROMUEVE al pipeline (Oportunidad). Devuelve
    cuántas registró."""
    if not (IMAP_HOST and SMTP_USER and SMTP_PASSWORD):
        logger.warning("[inbox] IMAP no configurado.")
        return 0
    try:
        from imap_tools import MailBox, AND, MailMessageFlags
    except ImportError:
        logger.error("[inbox] falta la dependencia imap-tools.")
        return 0

    propio = db is None
    db = db or SessionLocal()
    registradas = 0
    try:
        # mark_seen=False: NO marcamos leído en el fetch. Solo marcamos 'seen' tras
        # commitear en la DB; si el commit falla, el mail queda no-leído y se reprocesa.
        with MailBox(IMAP_HOST, port=IMAP_PORT).login(SMTP_USER, SMTP_PASSWORD, "INBOX") as mailbox:
            for msg in mailbox.fetch(AND(seen=False), mark_seen=False):
                remitente = (msg.from_ or "").lower().strip()
                texto = (msg.text or msg.html or "")[:4000]
                if not remitente:
                    continue
                c = (db.query(Contacto)
                       .filter(Contacto.email.ilike(remitente))
                       .order_by(Contacto.created_at.desc())
                       .first())
                if not c:
                    continue
                c.respuesta_recibida = texto
                c.estado = "respondido"
                # Promoción al pipeline (import diferido para evitar ciclo con el router).
                from app.routers.crm import _promover_contacto
                _promover_contacto(c, db)
                try:
                    db.commit()
                except Exception:
                    db.rollback()
                    logger.error(f"[inbox] commit falló para {remitente}; se reprocesará.")
                    continue
                # recién ahora marcamos el mail como leído en el servidor IMAP
                try:
                    mailbox.flag(msg.uid, MailMessageFlags.SEEN, True)
                except Exception as e:
                    logger.warning(f"[inbox] no se pudo marcar SEEN {remitente}: {e}")
                registradas += 1
                logger.info(f"[inbox] respuesta de {remitente} → {c.empresa} (promovido al pipeline)")
        if registradas:
            logger.info(f"[inbox] {registradas} respuesta(s) registrada(s).")
        return registradas
    except Exception as e:
        logger.error(f"[inbox] error leyendo IMAP: {e}")
        return 0
    finally:
        if propio:
            db.close()
