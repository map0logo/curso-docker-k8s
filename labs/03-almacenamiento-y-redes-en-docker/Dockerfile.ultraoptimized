# Desafío: Dockerfile ultra-optimizado
FROM python:3.11-alpine as builder

WORKDIR /app

COPY . .

# Instalar compiladores temporales
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    linux-headers

# Remover compiladores
RUN apk del .build-deps

# --- Runtime ---
FROM python:3.11-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /app .

# Configurar permisos
RUN chown -R appuser:appgroup /app

ENV PATH=/root/.local/bin:$PATH:/home/appuser/.local/bin

USER appuser

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# Variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]