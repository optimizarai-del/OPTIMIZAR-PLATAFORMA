"""
Scheduler del outreach. Dispara el envío (1×/día) y la escucha del inbox (cada X minutos)
dentro del proceso de la app, sin n8n ni cron externo.

Se activa solo si OUTREACH_ENABLED=true → en local/dev queda apagado por defecto.
Asume un único worker de uvicorn (caso típico de este deploy). Con múltiples workers,
mover a un proceso worker dedicado para no duplicar envíos.
"""
import os
import logging

logger = logging.getLogger(__name__)

_scheduler = None


def start_scheduler():
    global _scheduler
    from app.outreach_service import OUTREACH_ENABLED, enviar_pendientes, revisar_inbox

    if not OUTREACH_ENABLED:
        logger.info("[scheduler] OUTREACH_ENABLED=false → outreach automático apagado.")
        return None

    try:
        from apscheduler.schedulers.background import BackgroundScheduler
    except ImportError:
        logger.error("[scheduler] falta apscheduler; no se programa el outreach.")
        return None

    tz = os.getenv("OUTREACH_TZ", "America/Argentina/Buenos_Aires")
    hora_envio = int(os.getenv("OUTREACH_SEND_HOUR", "9"))
    inbox_cada_min = int(os.getenv("OUTREACH_INBOX_EVERY_MIN", "10"))

    sched = BackgroundScheduler(timezone=tz)
    sched.add_job(enviar_pendientes, "cron", hour=hora_envio, minute=0,
                  id="enviar_pendientes", replace_existing=True, max_instances=1)
    sched.add_job(revisar_inbox, "interval", minutes=inbox_cada_min,
                  id="revisar_inbox", replace_existing=True, max_instances=1)
    sched.start()
    _scheduler = sched
    logger.info(f"[scheduler] outreach activo — envío {hora_envio}:00 {tz}, inbox cada {inbox_cada_min}min.")
    return sched
