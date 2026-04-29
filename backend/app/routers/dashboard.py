from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.database import get_db
from app.models import Proyecto, Tarea, Requerimiento, RegistroTiempo, ProyectoStatus, TareaStatus, RequerimientoStatus
from app.schemas import DashboardHUD
from app.security import get_db_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/hud", response_model=DashboardHUD)
def hud(db: Session = Depends(get_db), _=Depends(get_db_user)):
    total_proyectos = db.query(Proyecto).count()
    proyectos_activos = db.query(Proyecto).filter(Proyecto.status == ProyectoStatus.en_progreso).count()
    total_tareas = db.query(Tarea).count()
    tareas_pendientes = db.query(Tarea).filter(Tarea.status == TareaStatus.pendiente).count()
    tareas_completadas = db.query(Tarea).filter(Tarea.status == TareaStatus.completada).count()
    total_requerimientos = db.query(Requerimiento).count()
    requerimientos_nuevos = db.query(Requerimiento).filter(
        Requerimiento.status == RequerimientoStatus.nuevo
    ).count()

    semana_inicio = date.today() - timedelta(days=7)
    registros_semana = db.query(RegistroTiempo).filter(
        RegistroTiempo.fecha >= semana_inicio
    ).all()
    minutos_semana = sum(r.minutos for r in registros_semana)

    return {
        "total_proyectos": total_proyectos,
        "proyectos_activos": proyectos_activos,
        "total_tareas": total_tareas,
        "tareas_pendientes": tareas_pendientes,
        "tareas_completadas": tareas_completadas,
        "total_requerimientos": total_requerimientos,
        "requerimientos_nuevos": requerimientos_nuevos,
        "horas_semana": round(minutos_semana / 60, 1),
    }
