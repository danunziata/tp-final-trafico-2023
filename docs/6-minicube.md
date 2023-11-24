# Kubernetes

Kubernetes es una plataforma de código abierto para gestionar aplicaciones en contenedores, automatizando su implementación, escalado y operación.

## Minikube

### Introduccion 

Minikube es una herramienta que facilita la ejecución de clústeres de Kubernetes en entornos locales, permitiendo a los desarrolladores probar y desarrollar aplicaciones en contenedores en su propia máquina.

### Requisitos

2 CPU o más
2 GB de memoria libre
20 GB de espacio libre de disco
Conexión a Internet
Contenedor o gestor de máquinas virtuales, tales como: Docker, QEMU, Hyperkit, Hyper-V, KVM, Parallels, Podman, VirtualBox o VMware Fusion/Workstation

### Instalacion

bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

bash
sudo install minikube-linux-amd64 /usr/local/bin/minikube

### Implementacion

Desde una terminal de Linux, iniciamos minikube con el driver de virtualbox. Por defecto minikube crea un solo nodo y con el driver Docker.

bash
minikube start --driver=virtualbox --memory=(ram) --cpus=(cantidad) --nodes=(cantidad de nodos)

`--driver` gestor de maquinas virtuales a utilizar 
`--memory` memoria ram en MB
`--nodes` cantidad de nodos (maquinas virtuales)
`--cpus` cantidad de nucleos de cpu  

Ver el estado de minikube:
bash
minikube status


Para ver informacion sobre nuestro cluster escribimos el comando:
bash
minikube profile list


Para detener minikube:
bash
minikube stop


Para eliminar todos nuestros nodos:
bash
minikube delete --all


ADDONS:
Conjuntos de componentes adicionales y configuraciones predefinidas que puedes habilitar fácilmente para extender la funcionalidad de tu clúster de Kubernetes local.

Administrar addons:
bash
minikube addons list


Activar addons:
bash
minikube addons enable (nombre del addons)


Ejemplo de algunos addons y para que sirven:

- Dashboard: Proporciona una interfaz web que permite visualizar y administrar recursos en tu clúster de Kubernetes.

- Metrics Server: Recopila métricas de recursos del clúster y las hace accesibles para consultas.

- Registry: Configura un registro de contenedores local en el clúster, lo que puede ser útil para probar imágenes personalizadas.

- Ingress: Facilita la exposición de servicios HTTP y HTTPS desde el clúster a través de reglas de enrutamiento.



## Kubectl

### Introduccion

Kubectl se utiliza para desplegar y gestionar aplicaciones en Kubernetes. Usando kubectl, puedes inspeccionar recursos del clúster; crear, eliminar, y actualizar componentes; explorar tu nuevo clúster y arrancar aplicaciones.

### Instalacion 

bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

Validar binario:
bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"

bash
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check

A la salida de este comando debe decir "la suma coincide".

bash
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl


Validar version:
bash
kubectl version --client


### Implementacion

Aplicar un archivo `.yaml`
bash
kubectl apply -f (archivo.yaml)

Para aplicar todos los archivos `.yaml` del directorio donde nos encontramos ubicados:
bash
kubectl apply -f .


Visualizar servicios:
bash
kubectl get svc


Visualizar pods:
bash
kubectl get pods


Visualizar todo lo que esta corriendo nuestro cluster:
bash
kubectl get all


## Archivos .yaml

### Introduccion

.yaml (YAML) es un formato de serialización de datos que se utiliza comúnmente para representar configuraciones y datos estructurados de manera legible para humanos. La sigla "YAML" significa "YAML Ain't Markup Language" o, de manera recursiva, "YAML Ain't a Markup Language". YAML es un formato simple y fácil de leer que utiliza espacios y sangrías para estructurar la información.
En el contexto de Kubernetes y otros sistemas de orquestación de contenedores, los archivos YAML son comúnmente utilizados para definir la configuración de los recursos, como despliegues, servicios, volúmenes, y más.

### Tipos de archivos .yaml

Los dos que deben implementarse si o si son:

- Deployments:
Un "Deployment" en Kubernetes es un objeto que permite declarar y gestionar la implementación de aplicaciones en un clúster. Proporciona funcionalidades como estrategias de despliegue, escalabilidad y rollbacks, facilitando la gestión del ciclo de vida de las aplicaciones en entornos contenerizados.
- Service:
Un "Service" en Minikube es como un operador de tráfico para tus aplicaciones en Kubernetes. Le da a tus aplicaciones una dirección fija y fácil de recordar para que puedan comunicarse entre sí sin importar dónde estén ejecutándose. También puede repartir el tráfico entre varias partes de tu aplicación para mantener las cosas equilibradas. En resumen, hace que sea más fácil para las partes de tu aplicación encontrarse y hablar entre sí.
