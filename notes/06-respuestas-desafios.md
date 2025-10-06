
## Parte 9: Preguntas de Reflexión

1. **¿Cuál es la diferencia principal entre ClusterIP, NodePort y LoadBalancer?**
   - **ClusterIP**: Solo accesible dentro del cluster
   - **NodePort**: Expone el servicio en un puerto específico de cada nodo
   - **LoadBalancer**: Crea un balanceador de carga externo (en cloud providers)

2. **¿Por qué es mejor usar Secrets en lugar de ConfigMaps para información sensible?**
   - Los Secrets se almacenan codificados en base64
   - Kubernetes ofrece mejor control de acceso para Secrets
   - Algunas distribuciones de K8s pueden encriptar Secrets en etcd
   - Mejores prácticas de seguridad

3. **¿Qué sucede si modificamos un ConfigMap después de desplegar la aplicación?**
   - Los pods existentes NO reciben los cambios automáticamente
   - Se debe reiniciar o recrear los pods para aplicar los cambios
   - Se puede usar herramientas como Reloader para actualización automática

4. **¿Cuándo usarías NodePort vs LoadBalancer?**
   - **NodePort**: Para desarrollo, pruebas locales, o cuando no hay soporte de LoadBalancer
   - **LoadBalancer**: En entornos cloud production con soporte de balanceadores externos

---