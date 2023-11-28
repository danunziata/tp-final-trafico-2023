# Implementacion en el cluster

### Seguir los pasos de la [pagina](https://danunziata.github.io/tp-final-trafico-2023/)

## 1)

Primero iniciamos un cluster en minikube con dos nodos
```bash
minikube start --memory=1800 --nodes=2
```

## 2)

Ubicados en la misma ruta donde se encuantran los 3 archivos .yaml iniciamos el deployment, el service y el HorizontalPodAutoscaler:

```bash
kubectl apply -f 01-service.yaml
```

A continuacion vemos el codigo:
```py
apiVersion: v1         #Indica que se está utilizando la versión 1 de la API de Kubernetes.
kind: Service          #Define el tipo de objeto Kubernetes que se está creando, en este caso, un servicio.
metadata:              #Contiene metadatos asociados al objeto, como el nombre del servicio.
  name: php-fastapi    #Nombre del servicio
spec:                  #Contiene la especificación del servicio, que incluye el tipo de servicio, los puertos expuestos y el conjunto de pods que el servicio debe enrutar.
  type: NodePort       #Indica que el servicio será accesible desde fuera del clúster a través de un puerto específico en cada nodo del clúster.
  ports:               #Define la configuración de los puertos. 
  - port: 8000         #El puerto que el servicio estará escuchando dentro del clúster.
    targetPort: 8000   #El puerto al que el tráfico del servicio será enviado dentro de los pods seleccionados.
    nodePort: 30000    #El puerto que estará abierto en cada nodo del clúster para acceder al servicio desde fuera del clúster.
  selector:            #Especifica qué pods serán seleccionados por este servicio. En este caso, los pods deben tener la etiqueta role: php-fastapi. 
    role: php-fastapi
```

Ahora iniciamos el deployment:
```bash
kubectl apply -f 02-deployment.yaml 
```

Con ```bash kubectl get all``` veremos si el servicio esta corriendo y los pods funcioinando correctamente (deben estar en `Running`).

Su codigo es el siguiente:
```py
apiVersion: apps/v1   #Indica que se está utilizando la versión 1 de la API de aplicaciones de Kubernetes.
kind: Deployment      #Define el tipo de objeto Kubernetes que se está creando, en este caso, un despliegue. Los despliegues gestionan la creación y actualización de instancias de aplicaciones en un clúster de Kubernetes.
metadata:             #Contiene metadatos asociados al objeto, como el nombre del despliegue. Aquí, el nombre del despliegue es "php-fastapi".
  name: php-fastapi   #
spec:                 #Contiene la especificación del despliegue, que incluye información sobre la replicación, el selector, la plantilla del pod y la configuración de los contenedores.
  replicas: 1         #
  selector:           #Especifica cómo el despliegue encuentra los pods que debe gestionar. Aquí, el despliegue seleccionará los pods que tienen la etiqueta role: php-fastapi.
    matchLabels:      #Indica que se deben seleccionar los pods cuyas etiquetas coincidan exactamente con las especificadas.
      role: php-fastapi
  template:           #Define la plantilla para la creación de nuevos pods.
    metadata:         #Define las etiquetas para los pods creados por este despliegue.
      labels:         #Define las etiquetas del pod.
        role: php-fastapi   #Establece una etiqueta llamada role con el valor php-fastapi. Esta etiqueta es utilizada para que el selector del despliegue pueda identificar los pods que debe gestionar.
    spec:             # Define la especificación del pod.
      containers:     #Describe la configuración del contenedor que se ejecutará en los pods.
      - name: php-fastapi   #Especifica el nombre del contenedor.
        image: damiangn/imagen_kevin:latest   # Indica la imagen del contenedor que se utilizará para ejecutar la aplicación.
        imagePullPolicy: IfNotPresent   # Especifica la política de extracción de la imagen del contenedor.    
        ports:   #Define los puertos que el contenedor expondrá.
        - containerPort: 8000
        command: ["/bin/sh", "-c", "uvicorn servidor:app --host 0.0.0.0 --port 8000"]   # Especifica el comando que se ejecutará al iniciar el contenedor. En este caso, inicia un servidor FastAPI utilizando uvicorn.
        env:   #Define la variable de entorno para el contenedor, como la contrasena MYSQL_ROOT_PASSWORD en este caso.
        - name: MYSQL_ROOT_PASSWORD
          value: "password"
        resources:
          requests:
            memory: "64Mi"   #Memoria del pod
            cpu: "200m"      #fraccion de CPU que tiene el nodo, en este caso 200 milinucleos.
          limits:
            memory: "128Mi"
            cpu: "500m"   #500 milinucleos
```

## 3) 

Ahora con `minikube addons list` podemos visualizar todos los addons que tiene minikube, debemos activar `metrics-server` para que el HorizontalPodAutoscaler pueda apuntar a las metricas del pod.
```bash
minikube addons enable metrics-server
```

## 4)

Recien despues de activar el addon levantamos el HPA:
```bash
kubeclt apply -f 03-HorizontalPodAutoscaler.yaml
```

El codigo es el siguiente:
```py
apiVersion: autoscaling/v2      #Indica que se está utilizando la versión 2 de la API de autoscaling de Kubernetes.
kind: HorizontalPodAutoscaler   #Especifica que se está creando un objeto de tipo HorizontalPodAutoscaler.
metadata:                       #Contiene metadatos asociados al objeto.
  name: php-fastapi             #Establece el nombre del HorizontalPodAutoscaler como "php-fastapi".
spec:                           #Contiene la especificación del HorizontalPodAutoscaler.
  scaleTargetRef:               #Especifica la referencia al recurso que se escalará automáticamente.
    apiVersion: apps/v1         #Indica que el recurso objetivo es de tipo Deployment en la versión 1 de la API de aplicaciones de Kubernetes.
    kind: Deployment            #Indica que el recurso objetivo es un Deployment.
    name: php-fastapi           #Especifica el nombre del Deployment que se escalará, en este caso, "php-fastapi".
  minReplicas: 1                #Establece el número mínimo de réplicas que el HorizontalPodAutoscaler debe mantener. En este caso, se especifica que debe haber al menos 1 réplica.
  maxReplicas: 15               #Establece el número máximo de réplicas que el HorizontalPodAutoscaler puede escalar. En este caso, se especifica que el número máximo es 15.
  metrics:                      #Define las métricas utilizadas para escalar automáticamente los pods.
  - type: Resource              #Indica que se utilizarán métricas de recursos, como CPU o memoria.
    resource:                   #Especifica la métrica de recurso que se utilizará.
      name: cpu                 #Utilizará la métrica de CPU.
      target:                   #Define el objetivo de la métrica.
        type: Utilization       #Indica que el objetivo es la utilización de recursos.
        averageUtilization: 30  #Establece el objetivo de utilización de CPU en un 30%. El HorizontalPodAutoscaler ajustará dinámicamente el número de réplicas para mantener la utilización promedio de CPU cerca de este valor. Si la utilización de CPU es superior al 30%, el escalador puede aumentar el número de réplicas para manejar la carga.
```

## 5)

Para visualizar la direccion IP de nuestro cluster ponemos `minikube ip`.

Con esta direccion y conociendo que el servicio esta expuesto en el puerto 30000 podremos acceder al servidor.

Se manda solicitudes al servidor con el siguiente programa hecho en python:
```py
import subprocess
import time

def enviar_solicitud():
    # Ejecutar el comando curl
    subprocess.run(["curl", "192.168.59.147:30000"])

# Bucle infinito
while True:
    enviar_solicitud()
```

## 6)

Activamos el addons `dashboard` con el comando:
```bash
minikube addons enable dashboard 
```

Una vez activado podremos visualizar las metricas del cluster escribiendo `minikube dashboard`.

Por defecto las metricas se actualizar a una tasa de 60 segundos, y en base a esto el HorizontalPodAutoscaler crea o elimina pods cada 5 minutos.
