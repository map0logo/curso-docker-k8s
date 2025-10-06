## Respuestas a las Preguntas de Reflexión (Parte 10)

### 1. **¿Por qué es importante usar StatefulSet en lugar de Deployment para bases de datos?**

Los StatefulSets son esenciales para bases de datos porque:
- **Identidad de red estable**: Cada pod mantiene un nombre de host predecible (postgres-statefulset-0, postgres-statefulset-1, etc.)
- **Almacenamiento persistente único**: Cada réplica obtiene su propio PersistentVolume que persiste entre reinicios
- **Despliegue ordenado**: Las réplicas se crean/eliminan en orden secuencial (0, 1, 2...)
- **Actualizaciones controladas**: Las actualizaciones se realizan de una réplica a la vez, minimizando el tiempo de inactividad
- **Escalado predecible**: Al escalar, cada nueva réplica obtiene su propio PVC con nombre único

### 2. **¿Qué sucedería si eliminamos el PVC después de tener datos?**

- **Pérdida permanente de datos**: Todos los datos almacenados en el volumen se perderían irreversiblemente
- **StatefulSet fallaría**: El pod no podría montar el volumen y entraría en estado CrashLoopBackOff
- **Recuperación compleja**: Requeriría restaurar desde backups o recrear completamente la base de datos
- **Depende de la política de reclaim**: Si el PV tiene `persistentVolumeReclaimPolicy: Delete`, el PV también se eliminaría

### 3. **¿Cómo manejaría Kubernetes el almacenamiento si escalamos el StatefulSet a múltiples réplicas?**

- **PVCs individuales**: Cada réplica (postgres-statefulset-0, -1, -2) obtendría su propio PVC único
- **Nomenclatura predecible**: Los PVCs se nombrarían como `postgres-pvc-postgres-statefulset-0`, `postgres-pvc-postgres-statefulset-1`, etc.
- **Volúmenes independientes**: Cada réplica tendría almacenamiento aislado, no compartido
- **Aprovisionamiento dinámico**: Si está configurado con StorageClass, se crearían nuevos PVs automáticamente para cada nueva réplica

### 4. **¿Cuál es la diferencia entre accessModes ReadWriteOnce vs ReadWriteMany?**

- **ReadWriteOnce (RWO)**: 
  - Solo un nodo puede montar el volumen en modo lectura/escritura
  - Ideal para bases de datos single-instance como PostgreSQL
  - Más común y ampliamente soportado

- **ReadWriteMany (RWX)**:
  - Múltiples nodos pueden montar el volumen simultáneamente en modo lectura/escritura
  - Necesario para aplicaciones clustered como algunos sistemas de archivos distribuidos
  - Menos común y requiere soporte específico del storage provider

## Respuestas a los Ejercicios Prácticos (Parte 9)

### Ejercicio 1: Escalar el StatefulSet

**Análisis del resultado:**
- **Escalado fallido**: `kubectl scale statefulset postgres-statefulset --replicas=2` falla porque necesitamos múltiples PVCs
- **Causa**: El StatefulSet actual solo tiene un PVC template configurado para una réplica
- **Solución**: Para escalar correctamente, necesitaríamos:
  - Configurar un volumeClaimTemplate en el StatefulSet
  - Tener suficiente capacidad de almacenamiento
  - Considerar la arquitectura de replicación de PostgreSQL

### Ejercicio 2: Insertar Más Datos y Probar Persistencia

**Resultado esperado:**
- Los nuevos registros ("Laura Sánchez", "Pedro Rodríguez") se insertan correctamente
- El conteo total aumenta de 4 a 6 empleados
- Los datos persisten después de recrear el pod

### Ejercicio 3: Verificar Configuración de Volúmenes

**Hallazgos esperados:**
- **PVC estado Bound**: `postgres-pvc` está correctamente vinculado a un PV
- **Capacidad utilizada**: Se muestra el espacio utilizado en `/var/lib/postgresql/data/`
- **StorageClass**: Usa `standard` (provisionador de Minikube)
- **Access Modes**: `ReadWriteOnce`

## Respuestas Adicionales a Desafíos Implícitos

### **¿Por qué usamos subPath en el volumeMount?**
```yaml
volumeMounts:
- name: postgres-storage
  mountPath: /var/lib/postgresql/data
  subPath: postgres  # ← ¿Por qué esto?
```
**Respuesta:** Para aislar los datos de PostgreSQL en un subdirectorio específico del volumen, permitiendo que el mismo volumen pueda ser usado por múltiples aplicaciones o para organizar mejor los datos.

### **¿Por qué el livenessProbe usa pg_isready?**
**Respuesta:** `pg_isready` es una herramienta específica de PostgreSQL que verifica no solo que el proceso esté corriendo, sino que la base de datos esté aceptando conexiones y operacional.

### **¿Cuándo usar StatefulSet vs Deployment?**
**Respuesta tentativa:**
- **Usar StatefulSet cuando**:
  - La aplicación requiere identidad de red estable y predecible
  - Necesita almacenamiento persistente único por pod
  - Requiere despliegue/actualización ordenado
  - Ejemplos: Bases de datos, sistemas de mensajería con estado

- **Usar Deployment cuando**:
  - Los pods son stateless e intercambiables
  - No requiere identidad de red estable
  - El almacenamiento es efímero o compartido
  - Ejemplos: Servicios web, APIs, aplicaciones sin estado

### **¿Qué ventajas tiene usar ConfigMap para postgresql.conf?**
**Respuesta:**
- **Versionado**: Los cambios en configuración pueden seguir el mismo versionado que el código
- **Auditoría**: Se puede trackear quién y cuándo modificó la configuración
- **Reutilización**: La misma configuración puede aplicarse a múltiples instancias
- **Separación de concerns**: La configuración está separada de la imagen de contenedor

Estas respuestas proporcionan una base sólida para entender los conceptos clave del laboratorio sobre aplicaciones con estado en Kubernetes. ¿Te gustaría que profundice en alguna respuesta específica?