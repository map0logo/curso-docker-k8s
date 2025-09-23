## **Programa del Curso: Despliegue de Aplicaciones Modernas con Docker y Kubernetes**

Este programa está diseñado para llevar a los participantes desde los conceptos fundamentales de la contenerización con Docker hasta la orquestación a gran escala con Kubernetes. Cada sesión de 4 horas combina teoría y práctica para asegurar una comprensión sólida y aplicable.

---

### **Sesión 1: Fundamentos de Docker y Contenedores**

* **Objetivos:**  
    
  * Comprender qué es la contenerización y sus ventajas sobre la virtualización tradicional.  
  * Entender la arquitectura y los componentes clave de Docker.  
  * Aprender a ejecutar y gestionar el ciclo de vida de contenedores básicos.


* **Contenido Teórico:**  
    
  * **Módulo 1: Introducción a Docker**  
    * ¿Qué es Docker y qué problema resuelve?  
    * Máquinas Virtuales vs. Contenedores  
    * Arquitectura de Docker: Cliente, Docker Daemon, Registros  
    * El flujo: Build, Share, Run  
  * **Módulo 2: Gestión Básica de Contenedores**  
    * Comandos esenciales: `docker run`, `docker ps`, `docker stop`, `docker start`, `docker rm`  
    * Acceder a los logs de un contenedor (`docker logs`)  
    * Ejecutar comandos dentro de un contenedor en ejecución (`docker exec`)

* **Laboratorio: Mi Primer Contenedor.**  
    1. Instalación de Docker Desktop.  
    2. Desplegar un contenedor de Nginx y acceder a la página de bienvenida desde el navegador.  
    3. Desplegar un contenedor de base de datos PostgreSQL.  
    4. Inspeccionar los contenedores en ejecución, revisar sus logs y eliminarlos de forma segura.

---

### **Sesión 2: Creación y Gestión de Imágenes con Dockerfile**

* **Objetivos:**  
    
  * Aprender a buscar y utilizar imágenes existentes de Docker Hub.  
  * Construir imágenes personalizadas de forma reproducible utilizando un `Dockerfile`.  
  * Entender las directivas clave de un `Dockerfile` y las mejores prácticas para crear imágenes eficientes y seguras.


* **Contenido Teórico:**  
    
  * **Módulo 3: Imágenes**  
    * Búsqueda de imágenes en repositorios como Docker Hub  
    * Anatomía de un `Dockerfile`  
    * Diferencias cruciales: `RUN` vs. `CMD` vs. `ENTRYPOINT`  
    * **Actualización:** Mejores prácticas:  
      * Optimización de capas (caching).  
      * Ejecutar contenedores como usuario no-root por seguridad  
      * Uso de `Multi-stage builds` para crear imágenes de producción ligeras y seguras

* **Laboratorio: Contenerizando una Aplicación Python**  
    1. Crear una aplicación "Hola Mundo" simple con Fast API.
    2. Escribir un `Dockerfile` básico para empaquetar la aplicación.  
    3. Construir la imagen y ejecutar un contenedor a partir de ella.  
    4. Refactorizar el `Dockerfile` para usar un `multi-stage build`, reduciendo significativamente el tamaño final de la imagen.

---

### **Sesión 3: Persistencia de Datos y Redes en Docker**

* **Objetivos:**  
    
  * Entender cómo persistir datos en Docker para que no se pierdan cuando un contenedor es eliminado.  
  * Conectar contenedores entre sí para crear aplicaciones multi-servicio.  
  * Exponer puertos de contenedores de forma segura.


* **Contenido Teórico:**  
    
  * **Módulo 4: Storage**  
    * La necesidad del almacenamiento persistente  
    * **Volume**: La forma preferida de persistir datos. Creación y gestión (`docker volume create`, `ls`, `rm`)  
    * **Bind Mounts**: Mapeo de directorios del host al contenedor, ideal para desarrollo  
  * **Módulo 5: Network**  
    * Conceptos básicos de redes en Docker  
    * Publicación de puertos (`-p` o  `--publish`)  
    * Redes `bridge` (por defecto y definidas por el usuario) para la comunicación entre contenedores

* **Laboratorio: Conectando un Backend con su Base de Datos.**  
    1. Reutilizar la aplicación FastAPI de la sesión anterior.  
    2. Desplegar un contenedor PostgreSQL con un volumen para persistir sus datos.  
    3. Crear una red `bridge` personalizada.  
    4. Conectar ambos contenedores a la misma red para que la aplicación FastAPI pueda comunicarse con la base de datos por su nombre.

---

### **Sesión 4: Orquestación Local con Docker Compose**

* **Objetivos:**  
    
  * Aprender a definir y gestionar aplicaciones compuestas por múltiples contenedores usando un único archivo de configuración.  
  * Simplificar el flujo de desarrollo y pruebas de una arquitectura de microservicios.


* **Contenido Teórico:**  
    
  * **Módulo 6: Docker Stacks y Compose file**  
    * ¿Qué es la orquestación de contenedores y por qué es necesaria?  
    * Introducción al archivo `docker-compose.yml`  
    * Definición de servicios, redes y volúmenes en Compose.  
    * Comandos clave: `docker-compose up`, `down`, `logs`, `exec`.

* **Laboratorio: Definiendo un Stack Completo.**  
    1. Tomar la aplicación de la Sesión 3 (FastAPI \+ PostgreSQL).  
    2. Crear un archivo `docker-compose.yml` que defina ambos servicios, la red personalizada y el volumen de la base de datos.  
    3. Añadir un tercer servicio, como pgAdmin, para gestionar la base de datos visualmente.  
    4. Levantar y destruir todo el stack con un solo comando.

---

### **Sesión 5: Introducción a Kubernetes y Objetos Fundamentales**

* **Objetivos:**  
    
  * Comprender la necesidad de un orquestador avanzado como Kubernetes.  
  * Conocer la arquitectura de un clúster de Kubernetes.  
  * Desplegar y gestionar la unidad de trabajo básica: el `Pod`, a través de `Deployments`.


* **Contenido Teórico:**  
    
  * **Módulo 7: Introducción a Kubernetes**  
    * ¿Qué es Kubernetes (K8s)?  
    * Arquitectura: Control Plane (API Server, Scheduler, etc.) y Nodos (Kubelet, Kube-proxy)  
  * **Módulo 8 y 9: Namespaces y Objetos**  
    * Introducción a `kubectl`, la herramienta de línea de comandos.  
    * **Namespaces**: Para aislar recursos en el clúster  
    * **Labels y Selectors**: La clave para conectar objetos en K8s  
    * **Pods**: La unidad de despliegue mínima  
    * **Deployments**: Para describir el estado deseado de la aplicación y gestionar réplicas y actualizaciones

* **Laboratorio: Desplegando mi Primera Aplicación en Kubernetes.**  
    1. Instalación de un clúster local (minikube, k3d, o Docker Desktop Kubernetes).  
    2. Usar `kubectl` para explorar el clúster.  
    3. Crear un `Deployment` usando la imagen de Nginx.  
    4. Escalar el `Deployment` para tener múltiples réplicas (Pods).  
    5. Simular una falla eliminando un Pod y observar cómo Kubernetes lo recrea automáticamente.

---

### **Sesión 6: Exponiendo Aplicaciones y Gestionando la Configuración**

* **Objetivos:**  
    
  * Aprender a exponer las aplicaciones que corren en el clúster para que sean accesibles.  
  * Gestionar la configuración de las aplicaciones de forma desacoplada y segura.


* **Contenido Teórico:**  
    
  * **Módulo 11: Networking en K8s**  
    * **Services**: Un punto de acceso estable para un conjunto de Pods  
    * Tipos de Services: `ClusterIP` (interno), `NodePort` (para pruebas) y `LoadBalancer` (para exposición externa en la nube).  
  * **Módulo 9: Objetos de Configuración**  
    * **ConfigMaps**: Para almacenar datos de configuración no sensibles  
    * **Secrets**: Para almacenar información sensible como contraseñas o claves de API  
    * Cómo inyectar ConfigMaps y Secrets en los Pods (como variables de entorno o archivos).

* **Laboratorio: Configuración y Exposición de un Deployment.**  
    1. Tomar el `Deployment` de la aplicación FastAPI de sesiones anteriores.  
    2. Crear un `ConfigMap` para la URL de la base de datos y un `Secret` para las credenciales.  
    3. Modificar el `Deployment` para que consuma esta configuración como variables de entorno.  
    4. Crear un `Service` de tipo `NodePort` o `LoadBalancer` para exponer la aplicación fuera del clúster y acceder a ella.

---

### **Sesión 7: Almacenamiento Persistente en Kubernetes**

* **Objetivos:**  
    
  * Comprender cómo gestionar el almacenamiento persistente para aplicaciones con estado (stateful) como las bases de datos.  
  * Aprender el ciclo de vida del almacenamiento en Kubernetes.


* **Contenido Teórico:**  
    
  * **Módulo 10: Storage en K8s**  
    * **Volumes**: El concepto de volúmenes en K8s  
    * **PersistentVolumes (PV)**: Un recurso de almacenamiento en el clúster.  
    * **PersistentVolumeClaims (PVC)**: Una solicitud de almacenamiento por parte de un usuario/aplicación.  
    * **StorageClasses**: Para el aprovisionamiento dinámico de PVs  
  * **Módulo 9: Controladores para Aplicaciones con Estado**  
    * **StatefulSets**: Un controlador especializado para aplicaciones que requieren identidad de red estable y almacenamiento persistente único, como bases de datos.

* **Laboratorio: Desplegando una Base de Datos con Estado.**  
    1. Crear una `PersistentVolumeClaim` (PVC) para solicitar almacenamiento.  
    2. Desplegar una base de datos PostgreSQL usando un `StatefulSet` que utilice la PVC creada.  
    3. Conectarse a la base de datos, insertar datos, eliminar el Pod y verificar que al ser recreado, los datos persisten gracias al volumen persistente.

---

### **Sesión 8: Enrutamiento Avanzado con Ingress y Cargas de Trabajo por Lotes**

* **Objetivos:**  
    
  * Gestionar el acceso HTTP/HTTPS a los servicios del clúster de una manera inteligente y centralizada.  
  * Conocer otros tipos de objetos de Kubernetes para diferentes cargas de trabajo.


* **Contenido Teórico:**  
    
  * **Módulo 12: Ingress**  
    * ¿Qué es un `Ingress` y por qué es mejor que un `Service` de tipo `LoadBalancer` para gestionar múltiples servicios?  
    * Componentes: El `Ingress Controller` (ej. Nginx, Traefik) y el recurso `Ingress`.  
    * Configurar enrutamiento basado en host y en ruta (path).  
  * **Módulo 9: Otros Controladores**  
    * **Jobs**: Para tareas que se ejecutan una vez y terminan  
    * **CronJobs**: Para tareas que se ejecutan de forma programada (ej. backups nocturnos)

* **Laboratorio: Despliegue de Múltiples Aplicaciones con un solo Punto de Entrada.**  
    1. Instalar un Ingress Controller (ej. NGINX Ingress Controller) en el clúster.  
    2. Desplegar dos aplicaciones web sencillas (ej. `app-uno` y `app-dos`), cada una con su `Deployment` y `Service` de tipo `ClusterIP`.  
    3. Crear un único recurso `Ingress` que enrute el tráfico de `mi-dominio.com/uno` hacia `app-uno` y `mi-dominio.com/dos` hacia `app-dos`.  
    4. (Opcional) Crear un `CronJob` que imprima "Hola Mundo" en los logs cada minuto.
