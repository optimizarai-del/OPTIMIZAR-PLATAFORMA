from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db, SessionLocal
from app.models import Tarea, RegistroTiempo, User, Proyecto, NotificacionTipo
from app.schemas import TareaCreate, TareaUpdate, TareaOut
from app.security import get_db_user
import app.email_service as mail

router = APIRouter(prefix="/api/tareas", tags=["tareas"])


def _enrich_tarea(t: Tarea) -> dict:
    minutos = sum(r.minutos for r in t.registros)
    asignado_nombre = t.asignado.nombre if t.asignado else None
    return {
        **{c.name: getattr(t, c.name) for c in t.__table__.columns},
        "minutos_trabajados": minutos,
        "asignado_nombre": asignado_nombre,
    }


def _get_proyecto_nombre(db: Session, proyecto_id: int) -> str:
    p = db.query(Proyecto).filter_by(id=proyecto_id).first()
    return p.nombre if p else "—"


def _get_user(db: Session, uid: Optional[int]) -> Optional[User]:
    if not uid:
        return None
    return db.query(User).filter_by(id=uid).first()


# ── Notificación en background (usa su propia sesión DB) ──────────────────────

def _bg_notif(tipo, email: str, asunto: str, html: str,
              tarea_id: Optional[int], user_id: Optional[int]) -> None:
    db = SessionLocal()
    try:
        mail.registrar_y_enviar(
            db=db, tipo=tipo,
            destinatario_email=email, asunto=asunto, html=html,
            tarea_id=tarea_id, destinatario_id=user_id,
        )
    finally:
        db.close()


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[TareaOut])
def listar(proyecto_id: Optional[int] = None, status: Optional[str] = None,
           db: Session = Depends(get_db), _=Depends(get_db_user)):
    q = db.query(Tarea)
    if proyecto_id:
        q = q.filter(Tarea.proyecto_id == proyecto_id)
    if status:
        q = q.filter(Tarea.status == status)
    return [_enrich_tarea(t) for t in q.order_by(Tarea.created_at.desc()).all()]


@router.post("/", response_model=TareaOut)
def crear(data: TareaCreate, bg: BackgroundTasks,
          db: Session = Depends(get_db), current_user: User = Depends(get_db_user)):
    t = Tarea(**data.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)

    # Notificar al asignado si existe y es distinto de quien crea
    if t.asignado_a:
        asignado = _get_user(db, t.asignado_a)
        if asignado and asignado.id != current_user.id:
            proyecto_nombre = _get_proyecto_nombre(db, t.proyecto_id)
            asunto, html = mail.template_tarea_asignada(t, proyecto_nombre, asignado.nombre)
            bg.add_task(_bg_notif, NotificacionTipo.tarea_asignada,
                        asignado.email, asunto, html, t.id, asignado.id)

    return _enrich_tarea(t)


@router.get("/{tid}", response_model=TareaOut)
def detalle(tid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    t = db.query(Tarea).filter_by(id=tid).first()
    if not t:
        raise HTTPException(404, "Tarea no encontrada")
    return _enrich_tarea(t)


@router.patch("/{tid}", response_model=TareaOut)
def editar(tid: int, data: TareaUpdate, bg: BackgroundTasks,
           db: Session = Depends(get_db),
           current_user: User = Depends(get_db_user)):
    t = db.query(Tarea).filter_by(id=tid).first()
    if not t:
        raise HTTPException(404, "Tarea no encontrada")

    updates = data.model_dump(exclude_unset=True)
    proyecto_nombre = _get_proyecto_nombre(db, t.proyecto_id)

    # Capturar valores anteriores ANTES de aplicar cambios
    status_anterior   = t.status.value if hasattr(t.status, 'value') else str(t.status)
    asignado_anterior = t.asignado_a
    titulo_anterior   = t.titulo
    desc_anterior     = t.descripcion
    prio_anterior     = t.prioridad.value if hasattr(t.prioridad, 'value') else str(t.prioridad)

    # Completada: setear fecha real
    if updates.get("status") == "completada" and not t.fecha_fin_real:
        updates["fecha_fin_real"] = date.today()

    for k, v in updates.items():
        setattr(t, k, v)
    db.commit()
    db.refresh(t)

    status_nuevo = t.status.value if hasattr(t.status, 'value') else str(t.status)

    # ── Detectar y enviar notificaciones pertinentes ──────────────────────────

    # 1. Reasignación
    nuevo_asignado_id = updates.get("asignado_a")
    if "asignado_a" in updates and nuevo_asignado_id != asignado_anterior:
        nuevo = _get_user(db, nuevo_asignado_id)
        if nuevo and nuevo.id != current_user.id:
            anterior = _get_user(db, asignado_anterior)
            anterior_nombre = anterior.nombre if anterior else None
            asunto, html = mail.template_reasignacion(
                t, proyecto_nombre, nuevo.nombre, anterior_nombre)
            bg.add_task(_bg_notif, NotificacionTipo.reasignacion,
                        nuevo.email, asunto, html, t.id, nuevo.id)

    # 2. Cambio de estado
    elif "status" in updates and status_nuevo != status_anterior:
        # Notificar al asignado actual
        asignado = _get_user(db, t.asignado_a)
        if asignado:
            asunto, html = mail.template_cambio_estado(
                t, proyecto_nombre, asignado.nombre, status_anterior, status_nuevo)
            bg.add_task(_bg_notif, NotificacionTipo.cambio_estado,
                        asignado.email, asunto, html, t.id, asignado.id)

        # Si se completó, notificar también al que hizo el cambio (si es distinto)
        if status_nuevo == "completada":
            asignado = _get_user(db, t.asignado_a)
            completado_por = current_user.nombre
            if current_user.id != (t.asignado_a or -1):
                # notificar al asignado que fue marcada completa por otro
                if asignado and asignado.id != current_user.id:
                    asunto2, html2 = mail.template_tarea_completada(
                        t, proyecto_nombre, asignado.nombre, completado_por)
                    bg.add_task(_bg_notif, NotificacionTipo.tarea_completada,
                                asignado.email, asunto2, html2, t.id, asignado.id)

    # 3. Detalles actualizados (título, descripción o prioridad)
    else:
        cambios = []
        if "titulo" in updates and updates["titulo"] != titulo_anterior:
            cambios.append(f"Título: <em>{titulo_anterior}</em> → <strong>{updates['titulo']}</strong>")
        if "descripcion" in updates and updates["descripcion"] != desc_anterior:
            cambios.append("Descripción actualizada")
        if "prioridad" in updates:
            p_nuevo = updates["prioridad"].value if hasattr(updates["prioridad"], 'value') else str(updates["prioridad"])
            if p_nuevo != prio_anterior:
                labels = {"baja":"Baja","media":"Media","alta":"Alta","urgente":"Urgente"}
                cambios.append(f"Prioridad: {labels.get(prio_anterior, prio_anterior)} → {labels.get(p_nuevo, p_nuevo)}")
        if "fecha_fin_estimada" in updates:
            cambios.append("Fecha estimada de entrega actualizada")

        if cambios:
            asignado = _get_user(db, t.asignado_a)
            if asignado and asignado.id != current_user.id:
                asunto, html = mail.template_detalles_actualizados(
                    t, proyecto_nombre, asignado.nombre, cambios)
                bg.add_task(_bg_notif, NotificacionTipo.detalles_actualizados,
                            asignado.email, asunto, html, t.id, asignado.id)

    return _enrich_tarea(t)


@router.delete("/{tid}")
def eliminar(tid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    t = db.query(Tarea).filter_by(id=tid).first()
    if not t:
        raise HTTPException(404, "Tarea no encontrada")
    db.delete(t)
    db.commit()
    return {"ok": True}
