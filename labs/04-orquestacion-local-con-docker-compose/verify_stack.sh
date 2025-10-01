#!/bin/bash

echo "🔍 Verificando el stack de Docker Compose..."

# Verificar que docker-compose.yml existe
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml no encontrado"
    exit 1
fi

echo "✅ docker-compose.yml encontrado"

# Verificar servicios
services=("api" "db" "pgadmin")
for service in "${services[@]}"; do
    if docker-compose ps | grep -q "$service"; then
        echo "✅ Servicio $service está corriendo"
    else
        echo "❌ Servicio $service NO está corriendo"
    fi
done

# Verificar conectividad de la API
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ API respondiendo correctamente"
else
    echo "❌ API NO responde"
fi

# Verificar base de datos
if docker-compose exec db pg_isready -U postgres > /dev/null; then
    echo "✅ Base de datos conectada"
else
    echo "❌ Base de datos NO conectada"
fi

echo "🎉 Verificación completada!"