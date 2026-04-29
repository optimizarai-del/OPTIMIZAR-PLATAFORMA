from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Proyecto, PuntoAccion, Tarea, TareaStatus, User, UserRole
from app.schemas import (ProyectoCreate, ProyectoUpdate, ProyectoOut,
                          PuntoAccionCreate, PuntoAccionUpdate, PuntoAccionOut)
from app.security import get_db_user

router = APIRouter(prefix="/api/proyectos", tags=["proyectos"])


def _enrich(p: Proyecto) -> dict:
    total_tareas = len(p.tareas)
    tareas_completadas = sum(1 for t in p.tareas if t.status == TareaStatus.completada)
    total_puntos = len(p.puntos_accion)
    puntos_completados = sum(1 for pt in p.puntos_accion if pt.completado)

    if total_puntos > 0:
        progreso = (puntos_completados / total_puntos) * 100
    elif total_tareas > 0:
        progreso = (tareas_completadas / total_tareas) * 100
    else:
        progreso = 0.0

    return {
        **p.__dict__,
        "progreso": round(progreso, 1),
        "total_tareas": total_tareas,
        "tareas_completadas": tareas_completadas,
        "total_puntos": total_puntos,
        "puntos_completados": puntos_completados,
    }


@router.get("/", response_model=List[ProyectoOut])
def listar(db: Session = Depends(get_db), _=Depends(get_db_user)):
    proyectos = db.query(Proyecto).order_by(Proyecto.created_at.desc()).all()
    return [_enrich(p) for p in proyectos]


@router.post("/", response_model=ProyectoOut)
def crear(data: ProyectoCreate, db: Session = Depends(get_db),
          current_user: User = Depends(get_db_user)):
    p = Proyecto(**data.model_dump(), created_by=current_user.id)
    db.add(p)
    db.commit()
    db.refresh(p)
    return _enrich(p)


@router.get("/{pid}", response_model=ProyectoOut)
def detalle(pid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    p = db.query(Proyecto).filter_by(id=pid).first()
    if not p:
        raise HTTPException(404, "Proyecto no encontrado")
    return _enrich(p)


@router.patch("/{pid}", response_model=ProyectoOut)
def editar(pid: int, data: ProyectoUpdate, db: Session = Depends(get_db),
           _=Depends(get_db_user)):
    p = db.query(Proyecto).filter_by(id=pid).first()
    if not p:
        raise HTTPException(404, "Proyecto no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return _enrich(p)


@router.delete("/{pid}")
def eliminar(pid: int, db: Session = Depends(get_db),
             current_user: User = Depends(get_db_user)):
    if current_user.role not in [UserRole.admin, UserRole.manager]:
        raise HTTPException(403, "Sin permisos")
    p = db.query(Proyecto).filter_by(id=pid).first()
    if not p:
        raise HTTPException(404, "Proyecto no encontrado")
    db.delete(p)
    db.commit()
    return {"ok": True}


# ── Puntos de Acción ──────────────────────────────────────────────────────────

@router.get("/{pid}/plan", response_model=List[PuntoAccionOut])
def listar_plan(pid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    return db.query(PuntoAccion).filter_by(proyecto_id=pid).order_by(PuntoAccion.orden).all()


@router.post("/{pid}/plan", response_model=PuntoAccionOut)
def agregar_punto(pid: int, data: PuntoAccionCreate, db: Session = Depends(get_db),
                  _=Depends(get_db_user)):
    p = db.query(Proyecto).filter_by(id=pid).first()
    if not p:
        raise HTTPException(404, "Proyecto no encontrado")
    punto = PuntoAccion(**data.model_dump(), proyecto_id=pid)
    db.add(punto)
    db.commit()
    db.refresh(punto)
    return punto


@router.patch("/{pid}/plan/{punto_id}", response_model=PuntoAccionOut)
def editar_punto(pid: int, punto_id: int, data: PuntoAccionUpdate,
                 db: Session = Depends(get_db), _=Depends(get_db_user)):
    punto = db.query(PuntoAccion).filter_by(id=punto_id, proyecto_id=pid).first()
    if not punto:
        raise HTTPException(404, "Punto no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(punto, k, v)
    db.commit()
    db.refresh(punto)
    return punto


@router.delete("/{pid}/plan/{punto_id}")
def eliminar_punto(pid: int, punto_id: int, db: Session = Depends(get_db),
                   _=Depends(get_db_user)):
    punto = db.query(PuntoAccion).filter_by(id=punto_id, proyecto_id=pid).first()
    if not punto:
        raise HTTPException(404, "Punto no encontrado")
    db.delete(punto)
    db.commit()
    return {"ok": True}
