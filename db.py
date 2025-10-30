# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config_db import get_database_url

DATABASE_URL = get_database_url()  # debe empezar por postgresql+psycopg://

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=5,
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener sesión en rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
