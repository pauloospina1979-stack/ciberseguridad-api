# app.py
from fastapi import FastAPI
from db import Base, engine

# 👇 Si tienes modelos (tablas) definidos, impórtalos aquí antes de crear las tablas
# from modelos import Usuario, Curso, Evaluacion  # Ejemplo

# ⚠️ Esta línea crea las tablas automáticamente si no existen
# (en producción se recomienda usar Alembic, pero para pruebas en Render puedes dejarlo así)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Ciberseguridad",
    version="1.0.0",
    description="API desplegada en Render con FastAPI, SQLAlchemy y psycopg3",
)

# 🏠 Ruta raíz
@app.get("/")
def root():
    return {"message": "API desplegada correctamente 🚀"}

# 🔍 Ruta de verificación de salud
@app.get("/health")
def health_check():
    return {"status": "ok"}
