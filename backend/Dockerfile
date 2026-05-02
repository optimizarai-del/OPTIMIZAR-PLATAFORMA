FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# --proxy-headers + --forwarded-allow-ips=* hacen que uvicorn respete los
# headers X-Forwarded-Proto / X-Forwarded-Host del reverse proxy de EasyPanel
# (Traefik). Sin esto, los redirects 307 de FastAPI (ej: /api/proyectos -> /api/proyectos/)
# salen con esquema http en el Location header y el browser los bloquea por mixed-content.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*"]
