"""
Migrador idempotente y portable (SQLite local + Postgres/Supabase prod).

`Base.metadata.create_all()` crea tablas faltantes pero NO altera tablas existentes.
Por eso, cuando se agregan columnas a un modelo ya desplegado (ej. los campos de outreach
del Equipo de Venta y Prospección en `oportunidades`), hay que agregarlas explícitamente.

Este migrador:
- Usa el inspector de SQLAlchemy para ver qué columnas existen → no depende de
  `ADD COLUMN IF NOT EXISTS` (que SQLite no soporta). Mismo código en ambos motores.
- Es idempotente: si la columna ya existe, no hace nada. Seguro para correr en cada deploy.
- Es aditivo y nullable: no toca ni bloquea los datos existentes.
"""
import logging
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

# Columnas que el modelo espera pero que pueden faltar en una BD ya desplegada.
# { tabla: { columna: definición SQL del tipo (+ default opcional) } }
COLUMNAS_ESPERADAS = {
    "oportunidades": {
        "idioma": "VARCHAR",
        "disparador": "TEXT",
        "mensaje_asunto": "VARCHAR",
        "mensaje_cuerpo": "TEXT",
        "outreach_status": "VARCHAR DEFAULT 'sin_contactar'",
        "respuesta_recibida": "TEXT",
    },
    "requerimientos": {
        "analisis_estado": "VARCHAR DEFAULT 'pendiente'",
        "servicio_match_id": "INTEGER",
        "analisis_justificacion": "TEXT",
        "analisis_confianza": "INTEGER",
        "analisis_at": "TIMESTAMP",
    },
}


def migrar_columnas_faltantes(engine: Engine) -> None:
    """Agrega columnas faltantes en tablas existentes. Llamar DESPUÉS de create_all()."""
    insp = inspect(engine)
    tablas = set(insp.get_table_names())

    for tabla, columnas in COLUMNAS_ESPERADAS.items():
        if tabla not in tablas:
            # La tabla aún no existe: create_all() la crea completa, no hay nada que migrar.
            continue
        existentes = {c["name"] for c in insp.get_columns(tabla)}
        faltantes = {col: tipo for col, tipo in columnas.items() if col not in existentes}
        if not faltantes:
            continue
        for col, tipo in faltantes.items():
            sql = f'ALTER TABLE {tabla} ADD COLUMN {col} {tipo}'
            try:
                with engine.begin() as conn:        # autocommit por bloque (compatible con pgbouncer)
                    conn.execute(text(sql))
                logger.info(f"[migrate] {tabla}: columna '{col}' agregada.")
            except Exception as e:
                # No abortar el arranque por una columna: registrar y seguir.
                logger.error(f"[migrate] no se pudo agregar {tabla}.{col}: {e}")
