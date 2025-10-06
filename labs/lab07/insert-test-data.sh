#!/bin/bash

NAMESPACE="database-lab"

echo "=== Inserción de datos paso a paso ==="

POSTGRES_POD=$(kubectl get pods -n $NAMESPACE -l app=postgres -o jsonpath='{.items[0].metadata.name}')
echo "Usando pod: $POSTGRES_POD"

# Paso 1: Verificar conexión
echo "1. Verificando conexión..."
kubectl exec -n $NAMESPACE $POSTGRES_POD -- psql -U admin -d mydatabase -c "SELECT '✅ Conexión exitosa' as status;"

# Paso 2: Listar tablas existentes
echo "2. Tablas existentes:"
kubectl exec -n $NAMESPACE $POSTGRES_POD -- psql -U admin -d mydatabase -c "\dt"

# Paso 3: Crear tabla
echo "3. Creando tabla test_data..."
kubectl exec -n $NAMESPACE $POSTGRES_POD -- psql -U admin -d mydatabase -c "
CREATE TABLE IF NOT EXISTS test_data (
    id SERIAL PRIMARY KEY,
    test_value VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"

# Paso 4: Verificar que la tabla se creó
echo "4. Verificando creación de tabla..."
kubectl exec -n $NAMESPACE $POSTGRES_POD -- psql -U admin -d mydatabase -c "\dt"

# Paso 5: Insertar datos
echo "5. Insertando datos de prueba..."
kubectl exec -n $NAMESPACE $POSTGRES_POD -- psql -U admin -d mydatabase -c "
INSERT INTO test_data (test_value) VALUES 
('Dato de prueba 1 - ' || now()),
('Dato de prueba 2 - ' || now()),
('Dato de prueba 3 - ' || now());"

# Paso 6: Verificar inserción
echo "6. Verificando datos insertados..."
kubectl exec -n $NAMESPACE $POSTGRES_POD -- psql -U admin -d mydatabase -c "SELECT * FROM test_data ORDER BY id;"

# Paso 7: Conteo final
echo "7. Conteo final:"
kubectl exec -n $NAMESPACE $POSTGRES_POD -- psql -U admin -d mydatabase -c "SELECT '✅ Total registros: ' || COUNT(*) as total FROM test_data;"

echo "=== Inserción completada exitosamente ==="
