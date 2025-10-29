FROM python:3.11-slim

WORKDIR /app

# Set environment variables to prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install psycopg2-binary==2.9.3  # Fuerza la instalación de la versión compatible
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8080
EXPOSE 8080

# Set the command to run the app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

