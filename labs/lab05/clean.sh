# Eliminar recursos específicos
kubectl delete -f deployment.yaml
kubectl delete -f redis-deployment.yaml

# O eliminar todo en el namespace
kubectl delete all --all

# Parar Minikube
minikube stop
