#!/bin/bash

# Build de la imagen
echo "Construyendo imagen Docker..."
docker build -t mi-fastapi-app:latest .

# Usar el docker daemon de minikube
echo "Configurando Docker para Minikube..."
eval $(minikube docker-env)

echo "Reconstruyendo imagen en Minikube..."
docker build -t mi-fastapi-app:latest .

# Redeploy
echo "Reiniciando deployment..."
kubectl rollout restart deployment/fastapi-deployment

# Esperar a que esté listo
echo "Esperando a que los pods estén ready..."
kubectl rollout status deployment/fastapi-deployment -w

echo "Despliegue completado!"
