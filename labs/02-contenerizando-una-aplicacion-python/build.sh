#!/bin/bash

set -e  # Detener en error

echo "=== Construyendo aplicación FastAPI ==="

# Variables
IMAGE_NAME="mi-fastapi-app"
TAG="latest"

# Limpiar contenedores previos
docker ps -aq --filter "name=fastapi-*" | xargs -r docker rm -f

# Construir imagen
echo "Construyendo imagen Docker..."
docker build -t $IMAGE_NAME:$TAG -f Dockerfile.multistage .

# Mostrar información de la imagen
echo "=== Información de la imagen ==="
docker images $IMAGE_NAME:$TAG

# Ejecutar tests básicos
echo "=== Ejecutando tests básicos ==="
docker run -d --name fastapi-test -p 8000:8000 $IMAGE_NAME:$TAG
sleep 10  # Esperar que la app inicie

# Test de health check
if curl -f http://localhost:8000/health; then
    echo "✅ Health check PASSED"
else
    echo "❌ Health check FAILED"
    docker logs fastapi-test
    exit 1
fi

# Test de endpoint principal
if curl -s http://localhost:8000/ | grep -q "Hola Mundo"; then
    echo "✅ Endpoint principal PASSED"
else
    echo "❌ Endpoint principal FAILED"
    exit 1
fi

# Limpiar
docker stop fastapi-test
docker rm fastapi-test

echo "=== Build completado exitosamente ==="
echo "Imagen: $IMAGE_NAME:$TAG"
echo "Tamaño: $(docker images $IMAGE_NAME:$TAG --format "table {{.Size}}" | tail -n1)"