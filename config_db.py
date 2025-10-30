# config_db.py
import os
from urllib.parse import quote_plus

def get_database_url() -> str:
    # Si ya tienes DATABASE_URL en el panel de Render, Respétala si trae el prefijo correcto.
    url = os.getenv("DATABASE_URL", "")

    # Si viene sin prefijo, lo corregimos a psycopg (v3)
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    if url.startswith("postgres://"):  # por compatibilidad antigua
        url = url.replace("postgres://", "postgresql+psycopg://", 1)

    # Alternativa: construir desde partes si no usas DATABASE_URL directa
    if not url:
        user = os.getenv("POSTGRES_USER", "")
        password = os.getenv("POSTGRES_PASSWORD", "")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "")
        url = f"postgresql+psycopg://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{db}"

    return url
