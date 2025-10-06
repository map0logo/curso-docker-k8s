#!/bin/bash
echo "=== Validación del Laboratorio ==="

# Verificar cluster
echo "1. Verificando cluster..."
minikube status > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Cluster Minikube funcionando"
else
    echo "✗ Error: Cluster no disponible"
fi

# Verificar deployments
echo "2. Verificando deployments..."
kubectl get deployment python-counter > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Deployment python-counter existe"
    REPLICAS=$(kubectl get deployment python-counter -o jsonpath='{.status.readyReplicas}')
    echo "✓ Réplicas activas: $REPLICAS"
else
    echo "✗ Deployment no encontrado"
fi

# Verificar servicios
echo "3. Verificando servicios..."
kubectl get service python-counter-service > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Servicio python-counter-service existe"
else
    echo "✗ Servicio no encontrado"
fi

# Test de conectividad
echo "4. Test de conectividad..."
SERVICE_URL=$(minikube service python-counter-service --url 2>/dev/null)
if curl -s $SERVICE_URL > /dev/null; then
    echo "✓ Aplicación accesible"
else
    echo "✗ Error de conectividad"
fi

echo "=== Validación completada ==="
