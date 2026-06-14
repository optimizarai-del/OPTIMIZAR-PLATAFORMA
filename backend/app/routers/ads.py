"""
Marketing · Meta Ads — métricas de anuncios y recomendaciones.

Flujo (mismo patrón que el Equipo de Venta y Prospección, sin API de Anthropic):
- El agente `meta-ads-analyst` (Claude Code + MCP de Meta Ads) corre sobre el plan,
  baja las campañas e insights de Meta, analiza, y EMPUJA acá vía endpoints externos
  (API key): `POST /external/sync` (campañas + métricas) y `POST /external/recommendations`.
- La plataforma guarda y la UI lee con JWT. Upsert idempotente por external_id / (campaña, fecha).
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import date, timedelta, datetime, timezone

from app.database import get_db
from app.models import AdCampaign, AdMetric, AdRecommendation
from app.schemas import (AdCampaignOut, AdMetricOut, AdRecommendationOut, AdsOverview,
                         AdSyncIn, AdRecommendationsIn)
from app.security import get_db_user, verify_api_key, require_editor

router = APIRouter(prefix="/api/ads", tags=["ads"])


def _rango(dias: int) -> date:
    return date.today() - timedelta(days=max(1, dias))


def _agregar(metricas: List[AdMetric]) -> dict:
    """Agrega una lista de métricas diarias en totales + promedios ponderados."""
    gasto = sum(m.gasto or 0 for m in metricas)
    impres = sum(m.impresiones or 0 for m in metricas)
    clicks = sum(m.clicks or 0 for m in metricas)
    conv = sum(m.conversiones or 0 for m in metricas)
    valor = sum(m.valor_conversiones or 0 for m in metricas)
    ctr = (clicks / impres * 100) if impres else 0.0
    cpc = (gasto / clicks) if clicks else 0.0
    cpm = (gasto / impres * 1000) if impres else 0.0
    roas = (valor / gasto) if gasto else 0.0
    return {
        "gasto_total": round(gasto, 2), "impresiones_total": impres,
        "clicks_total": clicks, "conversiones_total": round(conv, 2),
        "valor_total": round(valor, 2),
        "ctr_prom": round(ctr, 2), "cpc_prom": round(cpc, 2),
        "cpm_prom": round(cpm, 2), "roas_prom": round(roas, 2),
    }


# ── Lectura (JWT) ──────────────────────────────────────────────────────────────

@router.get("/overview", response_model=AdsOverview)
def overview(dias: int = 14, db: Session = Depends(get_db), _=Depends(get_db_user)):
    desde = _rango(dias)
    campañas = db.query(AdCampaign).all()
    metricas = db.query(AdMetric).filter(AdMetric.fecha >= desde).all()
    agg = _agregar(metricas)

    # serie diaria de gasto/conversiones
    serie: dict = {}
    for m in metricas:
        k = m.fecha.isoformat()
        s = serie.setdefault(k, {"fecha": k, "gasto": 0.0, "conversiones": 0.0})
        s["gasto"] += m.gasto or 0
        s["conversiones"] += m.conversiones or 0
    serie_list = [
        {"fecha": v["fecha"], "gasto": round(v["gasto"], 2),
         "conversiones": round(v["conversiones"], 2)}
        for v in sorted(serie.values(), key=lambda x: x["fecha"])
    ]

    ultima = max((c.ultima_sync for c in campañas), default=None)
    nuevas = db.query(AdRecommendation).filter_by(estado="nueva").count()
    return AdsOverview(
        conectado=bool(campañas),
        ultima_sync=ultima,
        rango_dias=dias,
        campanas_total=len(campañas),
        campanas_activas=sum(1 for c in campañas if c.estado == "ACTIVE"),
        gasto_total=agg["gasto_total"],
        impresiones_total=agg["impresiones_total"],
        clicks_total=agg["clicks_total"],
        conversiones_total=agg["conversiones_total"],
        ctr_prom=agg["ctr_prom"],
        cpc_prom=agg["cpc_prom"],
        cpm_prom=agg["cpm_prom"],
        roas_prom=agg["roas_prom"],
        recomendaciones_nuevas=nuevas,
        serie_gasto=serie_list,
    )


@router.get("/campaigns", response_model=List[AdCampaignOut])
def listar_campaigns(dias: int = 14, db: Session = Depends(get_db), _=Depends(get_db_user)):
    desde = _rango(dias)
    campañas = db.query(AdCampaign).order_by(AdCampaign.ultima_sync.desc()).all()
    out = []
    for c in campañas:
        ms = [m for m in c.metricas if m.fecha >= desde]
        agg = _agregar(ms)
        item = AdCampaignOut.model_validate(c, from_attributes=True)
        item.gasto_total = agg["gasto_total"]
        item.impresiones_total = agg["impresiones_total"]
        item.clicks_total = agg["clicks_total"]
        item.conversiones_total = agg["conversiones_total"]
        item.ctr_prom = agg["ctr_prom"]
        item.cpc_prom = agg["cpc_prom"]
        item.roas_prom = agg["roas_prom"]
        out.append(item)
    return out


@router.get("/campaigns/{cid}/metrics", response_model=List[AdMetricOut])
def metricas_campaign(cid: int, dias: int = 30, db: Session = Depends(get_db),
                      _=Depends(get_db_user)):
    desde = _rango(dias)
    if not db.query(AdCampaign).filter_by(id=cid).first():
        raise HTTPException(404, "Campaña no encontrada")
    return (db.query(AdMetric)
              .filter(AdMetric.campaign_id == cid, AdMetric.fecha >= desde)
              .order_by(AdMetric.fecha)
              .all())


@router.get("/recommendations", response_model=List[AdRecommendationOut])
def listar_recomendaciones(estado: Optional[str] = None, db: Session = Depends(get_db),
                           _=Depends(get_db_user)):
    q = db.query(AdRecommendation)
    if estado:
        q = q.filter(AdRecommendation.estado == estado)
    recos = q.order_by(AdRecommendation.created_at.desc()).all()
    out = []
    for r in recos:
        item = AdRecommendationOut.model_validate(r, from_attributes=True)
        item.campana_nombre = r.campaign.nombre if r.campaign else None
        out.append(item)
    return out


@router.patch("/recommendations/{rid}", response_model=AdRecommendationOut)
def decidir_recomendacion(rid: int, estado: str, db: Session = Depends(get_db),
                          _=Depends(require_editor)):
    if estado not in ("nueva", "aplicada", "descartada"):
        raise HTTPException(422, "Estado inválido (nueva/aplicada/descartada).")
    r = db.query(AdRecommendation).filter_by(id=rid).first()
    if not r:
        raise HTTPException(404, "Recomendación no encontrada")
    r.estado = estado
    db.commit(); db.refresh(r)
    item = AdRecommendationOut.model_validate(r, from_attributes=True)
    item.campana_nombre = r.campaign.nombre if r.campaign else None
    return item


# ── Sincronización externa (API Key) — la usa el agente analista ──────────────

@router.post("/external/sync", tags=["ads-external"])
def sync_externo(data: AdSyncIn, db: Session = Depends(get_db), _=Depends(verify_api_key)):
    """Upsert idempotente de campañas y sus métricas diarias. Lo llama el agente."""
    campañas_ok = metricas_ok = 0
    for c in data.campanas:
        camp = db.query(AdCampaign).filter_by(external_id=c.external_id).first()
        if not camp:
            camp = AdCampaign(external_id=c.external_id)
            db.add(camp)
        camp.nombre = c.nombre
        camp.plataforma = c.plataforma
        camp.estado = c.estado
        camp.objetivo = c.objetivo
        camp.cuenta_id = c.cuenta_id
        camp.cuenta_nombre = c.cuenta_nombre
        camp.presupuesto_diario = c.presupuesto_diario
        camp.moneda = c.moneda
        camp.ultima_sync = datetime.now(timezone.utc)
        try:
            db.commit()
        except IntegrityError:                       # carrera en el create
            db.rollback()
            camp = db.query(AdCampaign).filter_by(external_id=c.external_id).first()
            if not camp:
                continue
        db.refresh(camp)
        campañas_ok += 1

        for m in c.metricas:
            met = (db.query(AdMetric)
                     .filter_by(campaign_id=camp.id, fecha=m.fecha)
                     .first())
            if not met:
                met = AdMetric(campaign_id=camp.id, fecha=m.fecha)
                db.add(met)
            for campo, val in m.model_dump().items():
                if campo == "fecha":
                    continue
                setattr(met, campo, val)
            metricas_ok += 1
        db.commit()
    return {"campanas": campañas_ok, "metricas": metricas_ok}


@router.post("/external/recommendations", tags=["ads-external"])
def recomendaciones_externas(data: AdRecommendationsIn, db: Session = Depends(get_db),
                             _=Depends(verify_api_key)):
    """Upsert idempotente de recomendaciones por external_id. No pisa la decisión humana
    (si ya está 'aplicada'/'descartada', solo actualiza el contenido, no resetea el estado)."""
    creadas = actualizadas = 0
    for r in data.recomendaciones:
        camp = None
        if r.campaign_external_id:
            camp = db.query(AdCampaign).filter_by(external_id=r.campaign_external_id).first()
        reco = db.query(AdRecommendation).filter_by(external_id=r.external_id).first()
        nueva = reco is None
        if nueva:
            reco = AdRecommendation(external_id=r.external_id, estado="nueva")
            db.add(reco)
        reco.campaign_id = camp.id if camp else None
        reco.tipo = r.tipo
        reco.severidad = r.severidad
        reco.titulo = r.titulo
        reco.detalle = r.detalle
        reco.accion_sugerida = r.accion_sugerida
        reco.metricas_clave = r.metricas_clave or {}
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            continue
        creadas += 1 if nueva else 0
        actualizadas += 0 if nueva else 1
    return {"creadas": creadas, "actualizadas": actualizadas}
