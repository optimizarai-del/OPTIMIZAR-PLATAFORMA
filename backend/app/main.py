import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, users, proyectos, tareas, tiempo, requerimientos, dashboard, notificaciones

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Optimizar — Automatización · Eficiencia · Resultados", version="1.0.0")

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
