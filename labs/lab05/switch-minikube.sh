#!/bin/bash

PROFILE=${1:-"minikube"}

echo "Cambiando al perfil: $PROFILE"

# Limpiar variables anteriores
unset DOCKER_TLS_VERIFY
unset DOCKER_HOST
unset DOCKER_CERT_PATH
unset DOCKER_API_VERSION

# Cambiar perfil
minikube profile $PROFILE

# Configurar nuevo entorno
eval $(minikube docker-env)

echo "Perfil $PROFILE configurado. Variables Docker:"
env | grep DOCKER
