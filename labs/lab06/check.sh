#!/bin/bash

SERVICE_NAME="fastapi-nodeport-service"
NAMESPACE="default"

# Obtener información del servicio
echo "=== Información del Servicio ==="
kubectl get service $SERVICE_NAME -n $NAMESPACE

echo -e "\n=== Endpoints ==="
kubectl get endpoints $SERVICE_NAME -n $NAMESPACE

echo -e "\n=== Pods Detrás del Servicio ==="
kubectl get pods -n $NAMESPACE -o wide

# Obtener IP y Puerto
MINIKUBE_IP=$(minikube ip)
NODE_PORT=$(kubectl get service $SERVICE_NAME -n $NAMESPACE -o jsonpath='{.spec.ports[0].nodePort}')

echo -e "\n=== Testeando Balanceo de Carga ==="
echo "URL: http://$MINIKUBE_IP:$NODE_PORT/hostname"
echo ""

# Contar distribuciones
declare -A distribution
TOTAL_REQUESTS=30

for ((i=1; i<=$TOTAL_REQUESTS; i++)); do
  response=$(curl -s http://$MINIKUBE_IP:$NODE_PORT/hostname)
  pod_name=$(echo $response | grep -o '"pod_hostname":"[^"]*"' | cut -d'"' -f4)
  
  if [ -z "$pod_name" ]; then
    pod_name="unknown"
  fi
  
  ((distribution[$pod_name]++))
  echo "Request $i: $pod_name"
  sleep 0.5
done

echo -e "\n=== Resultados del Balanceo ==="
for pod in "${!distribution[@]}"; do
  count=${distribution[$pod]}
  percentage=$((count * 100 / TOTAL_REQUESTS))
  echo "$pod: $count requests ($percentage%)"
done

