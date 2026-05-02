import os
from dotenv import load_dotenv

# Load .env BEFORE importing routers, so module-level os.getenv() calls see the values.
# override=True ensures system env vars (which Windows may set as empty strings) don't shadow our .env.
load_dotenv(override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, users, proyectos, tareas, tiempo, requerimientos, dashboard, notificaciones

Base.metadata.create_all(bind=engine)

# redirect_slashes=False evita los 307 cuando se llama a /api/proyectos en lugar de /api/proyectos/.
# Esos redirects rompen llamadas cross-origin desde el frontend porque Chrome
# dropea el header Authorization en redirects entre subdominios distintos.
app = FastAPI(
    title="Optimizar — Automatización · Eficiencia · Resultados",
    version="1.0.0",
    redirect_slashes=False,
)

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in [auth, users, proyectos, tareas, tiempo, requerimientos, dashboard, notificaciones]:
    app.include_router(r.router)


@app.get("/health")
def health():
    return {"status": "ok", "brand": "Optimizar"}
