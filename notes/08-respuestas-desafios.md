# Respuestas Detalladas a los Desafíos del Laboratorio

## Respuesta al Desafío 1

**Pregunta**: ¿Qué comando usarías para ver información detallada de los nodos del cluster?

### Respuesta Completa:

```bash
# Comando principal para información detallada de nodos
kubectl describe nodes

# Alternativas útiles para diferentes niveles de detalle:

# 1. Información básica en formato amplio
kubectl get nodes -o wide

# 2. Información en formato YAML (muy detallado)
kubectl get nodes -o yaml

# 3. Información en formato JSON
kubectl get nodes -o json

# 4. Información específica sobre recursos
kubectl top nodes  # Requiere metrics-server instalado

# 5. Ver condiciones de los nodos
kubectl get nodes -o custom-columns="NAME:.metadata.name,STATUS:.status.conditions[?(@.type=='Ready')].status,TAINTS:.spec.taints,ROLES:.metadata.labels.kubernetes\.io/role"
```

### Información que obtendrás con `kubectl describe nodes`:

1. **Información básica del nodo**:
   - Nombre, etiquetas, anotaciones
   - Direcciones IP internas y externas

2. **Condiciones del nodo**:
   ```
   Conditions:
     Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
     ----             ------  -----------------                 ------------------                ------                       -------
     MemoryPressure   False   Tue, 15 Aug 2023 10:30:00 -0500   Tue, 15 Aug 2023 08:00:00 -0500   KubeletHasSufficientMemory   kubelet has sufficient memory available
     DiskPressure     False   Tue, 15 Aug 2023 10:30:00 -0500   Tue, 15 Aug 2023 08:00:00 -0500   KubeletHasNoDiskPressure     kubelet has no disk pressure
     PIDPressure      False   Tue, 15 Aug 2023 10:30:00 -0500   Tue, 15 Aug 2023 08:00:00 -0500   KubeletHasSufficientPID      kubelet has sufficient PID available
     Ready            True    Tue, 15 Aug 2023 10:30:00 -0500   Tue, 15 Aug 2023 08:00:00 -0500   KubeletReady                 kubelet is posting ready status
   ```

3. **Capacidad y asignación de recursos**:
   ```
   Capacity:
     cpu:                4
     ephemeral-storage:  61255492Ki
     memory:             8146828Ki
     pods:               110
   Allocatable:
     cpu:                4
     ephemeral-storage:  5645264293
     memory:             8044428Ki
     pods:               110
   ```

4. **Pods ejecutándose en el nodo**:
   - Lista de todos los pods y sus estados
   - Uso de recursos por pod

5. **Eventos del nodo**:
   - Historial de eventos importantes
   - Advertencias y errores

### Ejemplo de uso en troubleshooting:

```bash
# Si un nodo tiene problemas, puedes usar:
kubectl describe node <nombre-del-nodo>

# Ver solo los nodos que no están Ready
kubectl get nodes --field-selector=status.conditions[?(@.type=="Ready")].status!=True

# Ver la capacidad de CPU y memoria de todos los nodos
kubectl get nodes -o custom-columns="NAME:.metadata.name,CPU:.status.capacity.cpu,MEMORY:.status.capacity.memory"
```

## Respuesta al Desafío 2

**Pregunta**: ¿Cómo verificarías que los servicios pueden comunicarse entre sí dentro del cluster?

### Respuesta Completa:

Existen varias formas de verificar la conectividad entre servicios dentro del cluster Kubernetes:

### Método 1: Usando un Pod Temporal de Diagnóstico

```bash
# Crear un pod temporal para testing
kubectl run -it --rm network-test --image=alpine:latest -n lab-ingress -- /bin/sh

# Una vez dentro del contenedor, instalar herramientas de red
apk update && apk add curl bind-tools

# Probar conectividad con los servicios
curl http://app-uno-service.lab-ingress.svc.cluster.local:80
curl http://app-dos-service.lab-ingress.svc.cluster.local:80

# También puedes usar nslookup para resolver DNS
nslookup app-uno-service.lab-ingress.svc.cluster.local
nslookup app-dos-service.lab-ingress.svc.cluster.local

# O usando ping (si las aplicaciones responden a ICMP)
ping app-uno-service.lab-ingress.svc.cluster.local
```

### Método 2: Usando BusyBox (más ligero)

```bash
# Ejecutar busybox temporal
kubectl run -it --rm test-pod --image=busybox:1.35 -n lab-ingress -- /bin/sh

# Desde dentro del pod, probar conectividad
wget -qO- http://app-uno-service:80
wget -qO- http://app-dos-service:80

# Probar resolución DNS
nslookup app-uno-service
```

### Método 3: Verificación desde un Pod Existente

```bash
# Si ya tienes pods ejecutándose, puedes usar exec
kubectl exec -it <pod-name> -n lab-ingress -- /bin/sh

# Luego desde dentro del pod probar la conectividad
curl http://app-uno-service:80/health
curl http://app-dos-service:80/status
```

### Método 4: Script de Verificación Automatizada

```bash
#!/bin/bash
# script-verificacion-conectividad.sh

echo "=== Verificación de Conectividad entre Servicios ==="

# Verificar que los servicios existen
echo "1. Verificando servicios..."
kubectl get svc -n lab-ingress app-uno-service app-dos-service

# Crear pod temporal para testing
echo "2. Creando pod temporal de prueba..."
kubectl run -it --rm connectivity-test \
  --image=alpine:latest \
  --restart=Never \
  -n lab-ingress \
  -- sh -c '
  echo "Instalando herramientas..."
  apk add --no-cache curl bind-tools > /dev/null 2>&1
  
  echo "Probando resolución DNS..."
  nslookup app-uno-service
  nslookup app-dos-service
  
  echo "Probando conectividad HTTP..."
  echo "=== App Uno ==="
  curl -s http://app-uno-service:80 | head -n 2
  echo "=== App Dos ==="
  curl -s http://app-dos-service:80 | head -n 2
  
  echo "Verificación completada"
  '

echo "=== Fin de la verificación ==="
```

### Método 5: Verificación de Endpoints

```bash
# Verificar que los servicios tienen endpoints correctos
kubectl get endpoints -n lab-ingress

# Describir los servicios para ver detalles
kubectl describe svc app-uno-service -n lab-ingress
kubectl describe svc app-dos-service -n lab-ingress

# Verificar que los endpoints apuntan a pods correctos
kubectl get endpoints app-uno-service -n lab-ingress -o yaml
kubectl get endpoints app-dos-service -n lab-ingress -o yaml
```

### Método 6: Usando Network Policies para Diagnóstico

```yaml
# network-policy-test.yaml (solo para diagnóstico)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-allow-all
  namespace: lab-ingress
spec:
  podSelector: {}
  ingress:
  - {}
  egress:
  - {}
```

### Análisis de Problemas Comunes:

**Problema 1: DNS no resuelve**
```bash
# Si nslookup falla, verificar:
kubectl get pods -n kube-system | grep dns
kubectl logs -n kube-system <coredns-pod>
```

**Problema 2: Conexión rechazada**
```bash
# Verificar que los pods están corriendo
kubectl get pods -n lab-ingress -l app=app-uno

# Verificar logs de la aplicación
kubectl logs -n lab-ingress <app-uno-pod>

# Verificar que los puertos coinciden
kubectl describe svc app-uno-service -n lab-ingress
kubectl describe pod <app-uno-pod> -n lab-ingress
```

**Problema 3: Network Policies bloqueando tráfico**
```bash
# Verificar network policies existentes
kubectl get networkpolicies -n lab-ingress

# Describir políticas específicas
kubectl describe networkpolicy <policy-name> -n lab-ingress
```

### Comandos Avanzados de Diagnóstico:

```bash
# Verificar configuración de red del cluster
kubectl cluster-info dump | grep -i network

# Verificar configuración de CoreDNS
kubectl get configmap -n kube-system coredns -o yaml

# Probar conectividad a nivel de red entre nodos
kubectl get nodes -o wide
ping <node-ip>

# Verificar si hay problemas con el CNI (Container Network Interface)
kubectl get pods -n kube-system | grep -E "(flannel|calico|weave)"
```

### Script Completo de Validación:

```bash
#!/bin/bash
# comprehensive-connectivity-check.sh

NAMESPACE="lab-ingress"
SERVICES=("app-uno-service" "app-dos-service")

echo "=== Verificación Completa de Conectividad ==="

for service in "${SERVICES[@]}"; do
    echo "--- Verificando $service ---"
    
    # Verificar que el servicio existe
    if kubectl get svc -n $NAMESPACE $service > /dev/null 2>&1; then
        echo "✓ Servicio $service existe"
        
        # Verificar endpoints
        ENDPOINTS=$(kubectl get endpoints -n $NAMESPACE $service -o jsonpath='{.subsets[0].addresses[*].ip}')
        if [ -n "$ENDPOINTS" ]; then
            echo "✓ Endpoints encontrados: $ENDPOINTS"
        else
            echo "✗ No hay endpoints para $service"
        fi
    else
        echo "✗ Servicio $service no existe"
    fi
done

# Test de conectividad desde un pod temporal
echo "--- Test de conectividad desde pod temporal ---"
kubectl run -it --rm connectivity-test \
  --image=nicolaka/netshoot:latest \
  --restart=Never \
  -n $NAMESPACE \
  -- /bin/bash -c "
  echo '=== Test de DNS ==='
  nslookup app-uno-service
  nslookup app-dos-service
  
  echo '=== Test de conectividad HTTP ==='
  curl -s -o /dev/null -w 'App Uno: %{http_code}\n' http://app-uno-service:80/health
  curl -s -o /dev/null -w 'App Dos: %{http_code}\n' http://app-dos-service:80/status
  
  echo '=== Test de conectividad TCP ==='
  timeout 5 bash -c '</dev/tcp/app-uno-service/80' && echo 'App Uno: Puerto 80 accesible' || echo 'App Uno: Puerto 80 no accesible'
  timeout 5 bash -c '</dev/tcp/app-dos-service/80' && echo 'App Dos: Puerto 80 accesible' || echo 'App Dos: Puerto 80 no accesible'
  "

echo "=== Verificación completada ==="
```

Estas verificaciones te permitirán identificar rápidamente cualquier problema de conectividad entre servicios en tu cluster Kubernetes y tomar las acciones correctivas necesarias.


# Solución: Error 404 Not Found - Configuración de Paths

El error 404 indica que el Ingress Controller (nginx) está recibiendo la petición, pero no encuentra la ruta configurada. Esto es comúnmente un problema de configuración de los paths en el recurso Ingress.

## Diagnóstico y Solución

### Paso 1: Verificar la Configuración Actual del Ingress

```bash
# Ver la configuración actual del Ingress
kubectl get ingress main-ingress -n lab-ingress -o yaml
```

### Paso 2: Problema Común - Configuración de Host

El problema más probable es que tu Ingress esté configurado con `host: mi-dominio.com` pero estés accediendo directamente por IP. Veamos la solución:

**Opción A: Modificar el Ingress para quitar el host (Recomendado para testing)**

```bash
# Editar el ingress
kubectl edit ingress main-ingress -n lab-ingress
```

**Reemplaza esto:**
```yaml
rules:
- host: mi-dominio.com
  http:
    paths:
    - path: /uno
      pathType: Prefix
      backend:
        service:
          name: app-uno-service
          port:
            number: 80
```

**Por esto:**
```yaml
rules:
- http:  # ← Quitar el host
    paths:
    - path: /uno
      pathType: Prefix
      backend:
        service:
          name: app-uno-service
          port:
            number: 80
    - path: /dos
      pathType: Prefix
      backend:
        service:
          name: app-dos-service
          port:
            number: 80
```

**Opción B: Aplicar un nuevo Inress corregido:**

```yaml
# ingress-corregido.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
  namespace: lab-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  ingressClassName: nginx
  rules:
  - http:  # Sin host específico para testing
      paths:
      - path: /uno
        pathType: Prefix
        backend:
          service:
            name: app-uno-service
            port:
              number: 80
      - path: /dos
        pathType: Prefix
        backend:
          service:
            name: app-dos-service
            port:
              number: 80
```

```bash
kubectl apply -f ingress-corregido.yaml
```

### Paso 3: Verificación Rápida

```bash
# Verificar que el cambio se aplicó
kubectl describe ingress main-ingress -n lab-ingress

# Ahora probar de nuevo
curl -v http://$(minikube ip):31569/uno

# También probar la raíz
curl -v http://$(minikube ip):31569/
```

### Paso 4: Solución Alternativa - Usar Header Host

Si prefieres mantener el host, puedes simularlo con curl:

```bash
# Usar el header Host para simular el dominio
curl -v -H "Host: mi-dominio.com" http://$(minikube ip):31569/uno
```

### Paso 5: Verificación Completa del Estado

Ejecuta este diagnóstico completo:

```bash
#!/bin/bash
echo "=== DIAGNÓSTICO COMPLETO ==="

echo "1. Verificando Ingress:"
kubectl get ingress -n lab-ingress -o wide

echo "2. Descripción detallada:"
kubectl describe ingress main-ingress -n lab-ingress

echo "3. Verificando servicios:"
kubectl get svc -n lab-ingress

echo "4. Verificando pods:"
kubectl get pods -n lab-ingress -o wide

echo "5. Verificando endpoints:"
kubectl get endpoints -n lab-ingress

echo "6. Probando conectividad directa a los servicios:"
# Obtener un pod de app-uno
APP_UNO_POD=$(kubectl get pods -n lab-ingress -l app=app-uno -o jsonpath='{.items[0].metadata.name}')
echo "Pod app-uno: $APP_UNO_POD"

# Ejecutar curl desde dentro del cluster
kubectl exec -it $APP_UNO_POD -n lab-ingress -- curl -s http://app-uno-service:80/

echo "=== FIN DIAGNÓSTICO ==="
```

### Paso 6: Si el Problema Persiste - Reinicio Completo

```bash
# Eliminar y recrear el ingress
kubectl delete ingress main-ingress -n lab-ingress

# Aplicar la versión corregida
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: main-ingress
  namespace: lab-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /uno
        pathType: Prefix
        backend:
          service:
            name: app-uno-service
            port:
              number: 80
      - path: /dos
        pathType: Prefix
        backend:
          service:
            name: app-dos-service
            port:
              number: 80
EOF

# Esperar 30 segundos y probar
sleep 30
curl -v http://$(minikube ip):31569/uno
```

### Comandos de Prueba Inmediatos:

**Prueba esto primero (más simple):**
```bash
# Editar rápidamente el ingress
kubectl patch ingress main-ingress -n lab-ingress -p '{"spec":{"rules":[{"http":{"paths":[{"path":"/uno","pathType":"Prefix","backend":{"service":{"name":"app-uno-service","port":{"number":80}}}}},{"path":"/dos","pathType":"Prefix","backend":{"service":{"name":"app-dos-service","port":{"number":80}}}}]}}]}}'

# Probar
curl -v http://$(minikube ip):31569/uno
```

**O prueba con el header Host:**
```bash
curl -v -H "Host: mi-dominio.com" http://$(minikube ip):31569/uno
```

### Verificación de que las Aplicaciones Funcionan Internamente

Antes de continuar, verifiquemos que las aplicaciones están funcionando correctamente:

```bash
# Probar acceso directo a los servicios desde dentro del cluster
kubectl run -it --rm test-pod --image=curlimages/curl -n lab-ingress -- sh -c '
echo "=== Probando app-uno-service ==="
curl -s http://app-uno-service:80/

echo "=== Probando app-dos-service ==="
curl -s http://app-dos-service:80/
'
```

**¿Podrías ejecutar este comando de verificación interna y decirme qué resultado obtienes?** Esto nos ayudará a determinar si el problema está en las aplicaciones o específicamente en la configuración del Ingress.