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
from app.models import Oportunidad, EtapaOportunidad

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
    """Manda los correos de las oportunidades con outreach_status='escrito'.
    Respeta el tope diario y el throttling de warm-up. Devuelve cuántos envió."""
    propio = db is None
    db = db or SessionLocal()
    enviados = 0
    try:
        # Selección + CLAIM atómico: tomamos las filas con lock de fila (skip_locked en
        # Postgres; no-op en SQLite que serializa escrituras) y las marcamos 'enviando'
        # con commit ANTES de enviar. Así una corrida manual y el cron no toman el mismo
        # lote → no hay doble envío al mismo lead.
        q = (db.query(Oportunidad)
               .filter(Oportunidad.outreach_status == "escrito",
                       Oportunidad.contacto_email.isnot(None),
                       Oportunidad.mensaje_cuerpo.isnot(None))
               .order_by(Oportunidad.created_at)
               .limit(OUTREACH_DAILY_CAP))
        try:
            pendientes = q.with_for_update(skip_locked=True).all()
        except Exception:
            pendientes = q.all()          # motor sin FOR UPDATE: seguimos igual
        for op in pendientes:
            op.outreach_status = "enviando"
        db.commit()                        # claim confirmado

        total = len(pendientes)
        for i, op in enumerate(pendientes):
            err = _enviar_uno(op.contacto_email, op.mensaje_asunto, op.mensaje_cuerpo)
            if err is None:
                op.outreach_status = "enviado"
                if op.etapa == EtapaOportunidad.lead:
                    op.etapa = EtapaOportunidad.contactado
                db.commit()
                enviados += 1
                logger.info(f"[outreach] enviado a {op.contacto_email} ({op.empresa})")
            else:
                op.outreach_status = "escrito"   # liberar para reintentar
                db.commit()
                logger.error(f"[outreach] fallo enviando a {op.contacto_email}: {err}")
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
    """Lee respuestas nuevas (no leídas) del inbox por IMAP, matchea la oportunidad por
    email del remitente y la marca 'respondido'. Devuelve cuántas registró."""
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
                op = (db.query(Oportunidad)
                        .filter(Oportunidad.contacto_email.ilike(remitente))
                        .order_by(Oportunidad.created_at.desc())
                        .first())
                if not op:
                    continue
                op.respuesta_recibida = texto
                op.outreach_status = "respondido"
                if op.etapa == EtapaOportunidad.lead:
                    op.etapa = EtapaOportunidad.contactado
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
                logger.info(f"[inbox] respuesta de {remitente} → {op.empresa}")
        if registradas:
            logger.info(f"[inbox] {registradas} respuesta(s) registrada(s).")
        return registradas
    except Exception as e:
        logger.error(f"[inbox] error leyendo IMAP: {e}")
        return 0
    finally:
        if propio:
            db.close()
