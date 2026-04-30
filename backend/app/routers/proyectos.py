from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Proyecto, PuntoAccion, Tarea, TareaStatus, User, UserRole
from app.schemas import (ProyectoCreate, ProyectoUpdate, ProyectoOut,
                          PuntoAccionCreate, PuntoAccionUpdate, PuntoAccionOut,
                          GitHubRepoSet, GitHubSyncResult)
from app.security import get_db_user
import app.github_service as gh
import app.ai_service as ai

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


# ── GitHub Integration ────────────────────────────────────────────────────────

@router.put("/{pid}/github/repo", response_model=ProyectoOut)
def set_github_repo(pid: int, data: GitHubRepoSet, db: Session = Depends(get_db),
                    _=Depends(get_db_user)):
    p = db.query(Proyecto).filter_by(id=pid).first()
    if not p:
        raise HTTPException(404, "Proyecto no encontrado")
    repo = data.repo.strip().strip("/")
    if repo and not gh.validate_repo(repo):
        raise HTTPException(400, f"Repositorio '{repo}' no encontrado o sin acceso. Verificá que sea público o que GITHUB_TOKEN tenga permisos.")
    p.github_repo = repo or None
    p.github_last_sync = None
    p.github_last_commit_sha = None
    db.commit()
    db.refresh(p)
    return _enrich(p)


@router.post("/{pid}/github/sync", response_model=GitHubSyncResult)
def sync_github(pid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    p = db.query(Proyecto).filter_by(id=pid).first()
    if not p:
        raise HTTPException(404, "Proyecto no encontrado")
    if not p.github_repo:
        raise HTTPException(400, "El proyecto no tiene un repositorio GitHub configurado.")

    try:
        commits = gh.fetch_recent_commits(p.github_repo)
    except RuntimeError as e:
        raise HTTPException(502, str(e))

    tareas = db.query(Tarea).filter_by(proyecto_id=pid).all()
    plan = db.query(PuntoAccion).filter_by(proyecto_id=pid).order_by(PuntoAccion.orden).all()

    tareas_data = [{"id": t.id, "titulo": t.titulo, "descripcion": t.descripcion, "status": t.status.value} for t in tareas]
    plan_data   = [{"id": pt.id, "titulo": pt.titulo, "completado": pt.completado} for pt in plan]

    result = ai.analyze_commits(commits, tareas_data, plan_data)

    task_updates_applied = []
    for upd in result.get("task_updates", []):
        tarea = db.query(Tarea).filter_by(id=upd["id"], proyecto_id=pid).first()
        if tarea and tarea.status.value != upd["status"]:
            tarea.status = upd["status"]
            task_updates_applied.append(upd)

    plan_updates_applied = []
    for upd in result.get("plan_updates", []):
        punto = db.query(PuntoAccion).filter_by(id=upd["id"], proyecto_id=pid).first()
        if punto and punto.completado != upd["completado"]:
            punto.completado = upd["completado"]
            plan_updates_applied.append(upd)

    latest_sha = commits[0]["sha"] if commits else p.github_last_commit_sha
    p.github_last_sync = datetime.utcnow()
    p.github_last_commit_sha = latest_sha
    db.commit()

    return GitHubSyncResult(
        commits_analizados=len(commits),
        task_updates=task_updates_applied,
        plan_updates=plan_updates_applied,
        summary=result.get("summary", ""),
    )


@router.get("/{pid}/github/commits")
def get_commits(pid: int, db: Session = Depends(get_db), _=Depends(get_db_user)):
    p = db.query(Proyecto).filter_by(id=pid).first()
    if not p or not p.github_repo:
        raise HTTPException(400, "Sin repositorio configurado.")
    try:
        return gh.fetch_recent_commits(p.github_repo)
    except RuntimeError as e:
        raise HTTPException(502, str(e))
