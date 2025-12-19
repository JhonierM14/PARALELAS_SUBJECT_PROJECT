# Despliegue en Kubernetes (Minikube)
## Requisitos

- Docker
- kubectl
- Minikube

## Pasos

Se recomienda usar un namespace propio para el proyecto:

```
kubectl create namespace paralelas-project
kubectl config set-context --current --namespace=paralelas-project
```

1. Iniciar Minikube:
minikube start

2. Aplicar los manifiestos de Kubernetes
Asegúrate de estar en la raíz del proyecto:
kubectl apply -f infra/k8s

## Verificar estado:

kubectl get pods -n paralelas-project
kubectl get jobs -n paralelas-project
kubectl get svc -n paralelas-project

O, para listar todos los recursos en ese namespace:

kubectl get all -n paralelas-project

## Resultado esperado
ingest-job     Completed
analysis-job   Completed
api-deployment Running

## Exponer API y FRONTEND:
minikube service api-service -n paralelas-project
minikube service frontend-service -n paralelas-project

# Diagnóstico y logs ¡¡¡IMPORTANTE!!!
En caso de presentarse algun error al verificar el estado de los pods ejecutar:

kubectl logs analysis-job-...

#### Tambien para verificar dentro de kube --> ejecutar:
kubectl exec -it api-deployment-599c566b97-r9bj7 -- ls /data/raw

Notas importantes
- Todos los contenedores están conectados al PVC data-pvc, que contiene las carpetas raw/, processed/ y results/.

- El archivo icolcap.csv debe existir en /data/raw dentro del pod de la API para que analysis-job funcione correctamente.

En caso de ser necesario copiar manualmente el .csv al PVC:

````
kubectl cp data/raw/icolcap.csv api-deployment-599c566b97-r9bj7:/data/raw/icolcap.csv -n paralelas-project
```

## Eliminar todos los recursos
```
kubectl delete all --all -n paralelas-project
kubectl delete pvc data-pvc -n paralelas-project
kubectl delete namespace paralelas-project
```