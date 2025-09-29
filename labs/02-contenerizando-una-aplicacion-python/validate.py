#!/usr/bin/env python3
"""
Script de validación para el laboratorio Docker
"""

import requests
import docker
import sys
import time

def validate_basic_requirements():
    """Validar requisitos básicos del sistema"""
    print("🔍 Validando requisitos del sistema...")
    
    try:
        # Verificar que Docker está corriendo
        client = docker.from_env()
        client.ping()
        print("✅ Docker está funcionando")
    except Exception as e:
        print(f"❌ Error con Docker: {e}")
        return False
    
    return True

def validate_image_build():
    """Validar que la imagen se construye correctamente"""
    print("\n🔍 Validando construcción de imagen...")
    
    try:
        client = docker.from_env()
        
        # Verificar que Dockerfile existe
        import os
        if not os.path.exists('Dockerfile'):
            print("❌ Dockerfile no encontrado")
            return False
        
        # Construir imagen (usando cache si existe)
        image, logs = client.images.build(path='.', tag='fastapi-lab', rm=True)
        print("✅ Imagen construida exitosamente")
        
        # Verificar tamaño
        image_info = client.images.get('fastapi-lab')
        size_mb = image_info.attrs['Size'] / (1024 * 1024)
        print(f"📦 Tamaño de imagen: {size_mb:.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Error construyendo imagen: {e}")
        return False

def validate_container_runtime():
    """Validar que el contenedor funciona correctamente"""
    print("\n🔍 Validando ejecución del contenedor...")
    
    try:
        client = docker.from_env()
        
        # Ejecutar contenedor
        container = client.containers.run(
            'fastapi-lab',
            ports={'8000/tcp': 8000},
            detach=True,
            name='test-container'
        )
        
        # Esperar que la app inicie
        time.sleep(3)
        
        # Probar endpoints
        base_url = 'http://localhost:8000'
        
        try:
            # Test health endpoint
            response = requests.get(f'{base_url}/health', timeout=5)
            if response.status_code == 200:
                print("✅ Health endpoint funciona")
            else:
                print(f"❌ Health endpoint error: {response.status_code}")
                return False
            
            # Test main endpoint
            response = requests.get(base_url, timeout=5)
            if response.status_code == 200 and 'Hola Mundo' in response.text:
                print("✅ Endpoint principal funciona")
            else:
                print("❌ Endpoint principal no funciona correctamente")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error conectando a la aplicación: {e}")
            return False
        finally:
            # Limpiar
            container.stop()
            container.remove()
            
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando contenedor: {e}")
        return False

def validate_multi_stage():
    """Validar características de multi-stage build"""
    print("\n🔍 Validando multi-stage build...")
    
    try:
        client = docker.from_env()
        
        # Verificar que tenemos diferentes Dockerfiles
        dockerfiles = ['Dockerfile.basic', 'Dockerfile.optimized', 'Dockerfile.multistage']
        existing_files = [f for f in dockerfiles if os.path.exists(f)]
        
        if len(existing_files) >= 2:
            print(f"✅ Encontrados {len(existing_files)} Dockerfiles")
            
            # Comparar tamaños si hay múltiples versiones
            for dockerfile in existing_files:
                tag = f"test-{dockerfile.replace('.', '-')}"
                try:
                    client.images.build(path='.', dockerfile=dockerfile, tag=tag, rm=True)
                    image = client.images.get(tag)
                    size_mb = image.attrs['Size'] / (1024 * 1024)
                    print(f"   {dockerfile}: {size_mb:.1f} MB")
                    
                    # Limpiar imagen temporal
                    client.images.remove(tag)
                except:
                    pass
                    
            return True
        else:
            print("❌ Se esperaban múltiples Dockerfiles para comparación")
            return False
            
    except Exception as e:
        print(f"❌ Error validando multi-stage: {e}")
        return False

def main():
    """Función principal de validación"""
    print("=== VALIDACIÓN DEL LABORATORIO DOCKER ===\n")
    
    tests = [
        validate_basic_requirements,
        validate_image_build,
        validate_container_runtime,
        validate_multi_stage
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n=== RESULTADOS FINALES ===")
    print(f"Pruebas pasadas: {passed}/{total}")
    
    if passed == total:
        print("🎉 ¡Todos los tests pasaron! Laboratorio completado exitosamente.")
        return 0
    else:
        print("💡 Algunos tests fallaron. Revisa los mensajes de error.")
        return 1

if __name__ == '__main__':
    sys.exit(main())