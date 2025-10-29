FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# EXPOSE es opcional en Render, pero puedes dejarlo sin número o quitarlo.
# EXPOSE 8080

# ⚠️ Importante: usar $PORT que pone Render; ${PORT:-8080} usa 8080 solo si no existe.
CMD ["sh", "-c", "gunicorn -k uvicorn.workers.UvicornWorker -w 4 app:app -b 0.0.0.0:${PORT:-8080}"]
