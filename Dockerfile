FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalar dependencias del sistema que a veces requiere psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
# Gunicorn + UvicornWorker es robusto en producción
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "app:app", "-b", "0.0.0.0:8080"]

