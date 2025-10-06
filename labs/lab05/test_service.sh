#!/bin/bash

# Iniciar Minikube si no está corriendo
if ! minikube status | grep -q "Running"; then
    echo "Iniciando Minikube..."
    minikube start
fi

# Esperar a que esté listo
echo "Esperando a que los servicios estén listos..."
sleep 10

# Obtener URL del servicio
SERVICE_URL=$(minikube service python-counter-service --url)
echo "Testing service at: $SERVICE_URL"

# Realizar requests
for i in {1..10}; do
    curl -s $SERVICE_URL | grep "Visita número"
    sleep 1
done

