import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from db import Base, engine
from routers import modules, lessons, quizzes, attempts, progress, dashboard

load_dotenv()
origins = [o.strip() for o in os.getenv("API_CORS_ORIGINS", "*").split(",") if o]

app = FastAPI(title="SAFE-like API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# (Opcional) crear metadata si usas SQLAlchemy ORM para crear tablas
# Base.metadata.create_all(bind=engine)

app.include_router(modules.router)
app.include_router(lessons.router)
app.include_router(quizzes.router)
app.include_router(attempts.router)
app.include_router(progress.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "SAFE-like API"}
