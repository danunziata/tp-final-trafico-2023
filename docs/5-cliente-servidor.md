# Cliente - Servidor

El objetivo es desarrollar un modelo de colas M/M/1 donde el tiempo de interarribo y el largo de las tareas poseen distribucion exponencial. Se hizo uso de Locust como cliente generador de tráfico, mientras que el servidor es una aplicación creada con FastApi. Ver implementación en [README](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/README.md)

A continuación se presentan los conceptos de Locust y FastApi y su utilización. 
## Locust

### Introduccion

Locust en Linux es una herramienta de código abierto para realizar pruebas de carga y estrés en aplicaciones web. Se utiliza para simular un gran número de usuarios accediendo a una aplicación web al mismo tiempo, lo que ayuda a identificar y solucionar problemas de rendimiento y escalabilidad.

Locust es una herramienta de prueba de rendimiento escalable, programable y fácil de usar. Algunas de sus características son:

- Pruebas de Rendimiento: Locust permite medir el rendimiento de una aplicación web al simular la carga que podría experimentar en un entorno de producción. Esto ayuda a identificar cuellos de botella, problemas de escalabilidad y a optimizar el rendimiento.
- Identificación de Problemas: Al simular el comportamiento de usuarios reales, Locust ayuda a identificar problemas como tiempos de respuesta lentos, errores de servidor, y otros problemas de rendimiento que podrían afectar la experiencia del usuario.
- Escalabilidad: Locust permite evaluar cómo una aplicación maneja un aumento en el número de usuarios concurrentes. Esto es crucial para garantizar que la aplicación pueda escalar de manera efectiva a medida que la demanden este trabajoa aumenta.
- Monitoreo en Tiempo Real: Proporciona métricas en tiempo real durante las pruebas, lo que permite a los desarrolladores y equipos de operaciones obtener información inmediata sobre el comportamiento y el rendimiento del sistema.
- Configuración Flexible: Locust permite definir escenarios de prueba mediante código Python, brindando flexibilidad para adaptarse a situaciones específicas de uso. Esto incluye la capacidad de simular diferentes patrones de tráfico y comportamientos de usuario.
- Generación de Informes: Locust genera informes detallados que ayudan a interpretar los resultados de las pruebas. Esto facilita la identificación de áreas de mejora y proporciona datos valiosos para la toma de decisiones.

### Utilización
Locust se utiliza para generar tráfico externo con tasa de arribo de Poisson y tiempos de interarribo de paquetes con distribución exponencial, por lo tanto depende de un solo parámetro que es el valor medio.

Se hace uso de un paradigma cliente-servidor donde el cliente hace referencia a la generación de tráfico por parte de Locust, mientras que el servidor es Uvicorn.

### Instalación
Antes de instalar Locust, se necesita tener Python que, por lo general, está instalado en Linux, pero de lo contrario el comando es:
```bash
sudo apt-get install python3
```
En caso de no tener el gestor de paquetes de python
```bash
sudo apt install python3-pip
```
A continuación se indica el siguiente comando utilizado para instalar locust
```bash
pip install locust
```
### Implementacion
Creando un archivo cliente Locust:
```bash
touch cliente.py
```
Para realizar el script del cliente, primero realizamos uno con distribución exponencial de los tiempos de interarribo utilizando la librería de "time" por lo que era síncrona y se debía esperar la respuesta para enviar una nueva tarea. Se encuentra en el siguiente link de GitHub: [cliente_exp_time.py](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/cliente_exp_time.py)
```py
from locust import HttpUser, task, between
import time, random
lambd=100
class HelloWorldUser(HttpUser):
   
	@task
	def hello_world(self):
		a=random.expovariate(lambd)
		time.sleep(a)
		self.client.get("/")

```
En primer lugar se importan módulos `from locust import HttpUser, task, between`.

Luego, se define una variable llamada `lambd` con un valor de 100. Esta variable aparentemente representa la tasa de llegada (lambda) para la distribución exponencial.

Por otro lado, se define una clase `HelloWorldUser` que hereda de HttpUser. Esta clase representa un usuario virtual que realizará pruebas de carga en la aplicación web.

`@task`: Decorador que define una tarea llamada hello_world. La tarea simula el comportamiento de un usuario que realiza una solicitud a la raíz ("/") de la aplicación web.

Con `a` se genera tiempo de espera utilizando la distribución exponencial. La función random.expovariate genera números distribuidos exponencialmente con una tasa dada por lambd.

Espera Sincrónica: `time.sleep(a)` Hace que el usuario espere durante el tiempo generado (a). Esto simula el tiempo que un usuario real podría esperar entre solicitudes.

Realización de Solicitud HTTP:`self.client.get("/")`: Realiza una solicitud GET a la ruta "/" de la aplicación web utilizando el cliente HTTP proporcionado por Locust.

Por otro lado, también realizamos un programa que realiza solicitudes http con distribución uniforme y asincrono. Se encuentra en el siguiente link de GitHub: [cliente_unif_async.py](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/cliente_unif_async.py)
```py
from locust import HttpUser, task, between
import random, asyncio
#lambd=1000
class HelloWorldUser(HttpUser):

    @task
    def hello_world(self):
        asyncio.sleep(0.01)
        self.client.get("/")
```
Este es similiar al anterior, con la diferencia que el segundo script utiliza `asyncio.sleep`, lo que indica que la espera se maneja de manera asíncrona. Esto permite que otras tareas se ejecuten durante la espera, lo que puede ser útil en escenarios de carga donde se espera que múltiples usuarios realicen solicitudes simultáneamente.

Por último, hicimos un script con un programa de python que no se ejecuta con el generador de tráfico Locust. [Cliente_Final](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/Cliente_Final.py)
```py
import aiohttp
import asyncio
import random

# Lista para almacenar los tiempos de respuesta
response_times = []

async def send_request(session, host, port, path, user_id):
    url = f"http://{host}:{port}{path}"

    # Medir el tiempo antes de enviar la solicitud
    start_time = asyncio.get_event_loop().time()

    # Iniciar la solicitud sin esperar la respuesta
    async with session.get(url) as response:
        #Para hacer que no espere la respuesta del servidor quitar el comentario en la siguiente linea y comentar la otra seccion
        #-----pass

        #La siguientes lineas hacen que el cliente espere la respuesta 
        data = await response.text()
        #-----print(f"Response from server: {data}")
       

    # Medir el tiempo después de recibir la respuesta y almacenar el tiempo de respuesta
    end_time = asyncio.get_event_loop().time()
    response_time = end_time - start_time
    response_times.append(response_time)
    print(f"response time  {response_time}")

    # Mostrar el tiempo promedio cada 100 paquetes
    if len(response_times) % 100 == 0:
        average_response_time = sum(response_times) / len(response_times)
        print(f"Avg. response time after {len(response_times)} packets: {average_response_time} seconds")

async def generate_traffic(user_id, session, host, port, path, lambda_value):
    while True:
        # Esperar un tiempo según la distribución exponencial antes de comenzar
        inter_arrival_time = random.expovariate(lambda_value)
        #-----print(f"User {user_id}: Will wait for {inter_arrival_time} seconds before starting")

        await asyncio.sleep(inter_arrival_time)

        # Ejecutar la solicitud
        await send_request(session, host, port, path, user_id)

async def main():
    host = "192.168.1.109"
    port = 2023  # Reemplaza con el puerto correcto
    path = "/" # Reemplaza con la ruta correcta

    num_users = int(input("Ingrese la cantidad de usuarios: "))
    lambda_value = float(input("Ingrese el valor de lambda para la distribución exponencial: "))

    async with aiohttp.ClientSession() as session:
        user_tasks = [generate_traffic(user_id, session, host, port, path, lambda_value) for user_id in range(1, num_users + 1)]
        await asyncio.gather(*user_tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

Este tercer programa de cliente es generador de tráfico también con el objetivo de sustituir a Locust por varias cuestiones como aumento de RPS máximo. No entendimos bien el funcionamiento de Locust.

Explicando el programa: 

- Solicitudes de Usuarios: Se simulan usuarios que envían solicitudes al servidor web. Cada usuario espera un tiempo aleatorio antes de enviar una solicitud, imitando la llegada no uniforme de usuarios.

- Tiempo de Respuesta: Se mide el tiempo que tarda el servidor en responder a cada solicitud. Los tiempos de respuesta se almacenan en una lista llamada response_times.

- Cálculo del Tiempo Promedio: Cada vez que se alcanza un múltiplo de 100 solicitudes, se calcula y muestra el tiempo promedio de respuesta hasta ese momento.

- Configuración del Servidor: Se configura la dirección del servidor, el puerto y la ruta a la que se enviarán las solicitudes.

- Configuración de Usuarios y Ejecución: El usuario ingresa la cantidad de usuarios y un parámetro llamado lambda que afecta la frecuencia de llegada de los usuarios. Se utilizan asyncio y aiohttp para manejar las operaciones asíncronas y ejecutar las simulaciones de usuarios en paralelo.

### Ejecucion

Para ejecutarlo debemos estar situados en el directorio donde se encuentre el archivo cliente.py. Una vez allí, implementamos el siguiente comando:

```bash
locust -f “nombre del archivo.py”
```

Una vez iniciado eso, ir a la dirección que te aparece, por ejemplo
Starting web interface at http://0.0.0.0:8089 (accepting connections from all network interfaces)

Cuando ingresamos a esa dirección, deberíamos de ver la interfaz de locust donde podemos comenzar un nuevo test y debemos ingresar 3 parámetros:

- número de usuarios: Es el número máximo de usuarios al mismo tiempo en el sistema.
- Spawn rate:  Cantidad de usuarios que aparecen por segundo (dado que el código del cliente tiene una aparición exponencial hace que no sea de manera lineal)
- Host: debemos ingresar la ip y puerto del servidor (en este caso es http://192.168.1.199:2023). Si se realiza de manera local, dejar este campo vacío.

Debido a los problemas que se han tenido con este generador de tráfico, se ha utilizado como cliente y generador de tráfico al archivo de python que se muestra en el siguiente enlace:  [Cliente_Final](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/Cliente_Final.py)
## Fast API

### Introduccion
FastAPI es un moderno marco de desarrollo web para la construcción de APIs (Interfaces de Programación de Aplicaciones) con Python 3.7 o versiones posteriores. Fue creado por Sebastián Ramírez y se destaca por su rendimiento, facilidad de uso y generación automática de documentación interactiva.

Algunas de las características clave de FastAPI incluyen:

- Rendimiento: FastAPI es conocido por ser extremadamente rápido debido a su implementación basada en el estándar Starlette y el uso de Pydantic para la validación y la serialización de datos.
- Tipado Estático: Hace un amplio uso de las anotaciones de tipo de Python para proporcionar un sistema de tipado estático que facilita la detección temprana de errores y mejora la autocompletación en entornos de desarrollo.
- Generación Automática de OpenAPI y Swagger: FastAPI genera automáticamente documentación interactiva (Swagger) y una especificación OpenAPI para tu API, lo que facilita el entendimiento y la prueba de tus endpoints.
- Sintaxis Declarativa: El diseño de FastAPI permite una sintaxis clara y declarativa para definir rutas y modelos de datos, lo que simplifica el desarrollo de APIs de manera eficiente.
- Validación de Datos Integrada: Utiliza Pydantic para realizar la validación automática de datos de entrada y salida, garantizando la consistencia y la integridad de los datos que entran y salen de la API.
- Soporte para WebSockets: FastAPI ofrece soporte integrado para el protocolo WebSocket, permitiendo la construcción de aplicaciones en tiempo real.
- Seguridad Integrada: Proporciona herramientas integradas para manejar la autenticación y la autorización, incluyendo el uso de estándares como OAuth2 y JWT (JSON Web Tokens).
- Escalabilidad: Puede manejar de manera eficiente altas cargas de tráfico y escalar para adaptarse a las demandas de aplicaciones de gran envergadura.
### Utilizacion

Fast API se utiliza para generar la aplicacion del servidor, donde nos va a devolver los tiempos de ejecucion del script de python + los tiempos de espera de la variable.

### Instalación
En primer lugar se debe instalar FastApi con el siguiente comando:
```bash
pip install FastAPI
```

Luego, se necesita el servidor Uvicorn, por lo que se debe implementar la siguiente linea en el terminal:
```bash
pip install uvicorn
```
### Implementacion
En cuanto al servidor, también hay tres programas. Hemos realizado algunas pruebas con un programa cuyo servidor tenia un valor constante de `sleep` en lugar de ser una variable aleatoria con distribución exponencial. [servidor_unif_async.py](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/servidor_unif_async.py)
```py
from fastapi import FastAPI
#import random
import asyncio

app = FastAPI()
#mu = 100    # 1 / media

@app.get("/")
async def root():
    a = 0.01
    asyncio.sleep(a)
    return {1}
```
Este código define una aplicación FastAPI con una sola ruta ("/") que simula una pequeña espera antes de enviar una respuesta simple (un diccionario con el número 1) al cliente que realiza la solicitud. Este tipo de espera puede ser útil para simular ciertos comportamientos asíncronos en una aplicación web, aunque en este caso, la espera es fija en 0.01 segundos.

También realizamos un script con distribución exponencial asíncrono. [servidor_exp_async.py](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/servidor_exp_async.py)
```py
from fastapi import FastAPI
import random, asyncio
app = FastAPI()
mu = 100

@app.get("/")
async def root():
    a = random.expovariate(mu)
    asyncio.sleep(a)
    return {1}
```
Respecto del anterior, la principal diferencia entre ambos códigos radica en la generación del tiempo de espera. El segundo código utiliza una distribución exponencial para determinar dinámicamente el tiempo de espera antes de responder, mientras que el primer código utiliza un tiempo de espera fijo. Ambos códigos simulan la espera asincrónica antes de enviar una respuesta en una aplicación web utilizando FastAPI.

Por otro lado, también hemos realizado algunas pruebas con un programa cuyo servidor tenia una variable aleatoria con distribución exponencial sincrona. [servidor_exp_time.py](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/servidor_exp_time.py)
```py
from fastapi import FastAPI
import random, time
app = FastAPI()
mu = 100

@app.get("/")
async def root():
    a = random.expovariate(mu)
    time.sleep(a)
    return {1}
```

La diferencia clave entre este código y el anterior es la elección de la función de espera (time.sleep en lugar de asyncio.sleep), lo que afecta el comportamiento de espera y la capacidad de la aplicación para manejar múltiples solicitudes concurrentes de manera eficiente.

### Ejecucion
Una vez creado los programas tanto para el cliente como el servidor, para ejecutar es necesario utilizar el servidor Uvicorn para levantar la aplicación creada con FastApi.

Uvicorn es una implementación de servidor web ASGI (Asynchronous Server Gateway Interface) para Python. ASGI es una especificación que permite la creación de aplicaciones web asincrónicas en Python. Uvicorn es una implementación de referencia para esta especificación y está diseñado para trabajar con frameworks web asincrónicos como FastAPI.

Algunas características clave de Uvicorn incluyen:

- Asincronía: Uvicorn está diseñado para manejar operaciones de entrada/salida de manera eficiente mediante el uso de corutinas y el bucle de eventos asyncio.
- Compatibilidad con ASGI: Al ser un servidor ASGI, Uvicorn puede trabajar con aplicaciones web que sigan la especificación ASGI, permitiendo la construcción de aplicaciones web asincrónicas y eficientes en Python.
- Rendimiento: Uvicorn se esfuerza por ofrecer un rendimiento elevado y es capaz de manejar un gran número de conexiones concurrentes.
- Facilidad de Uso: Es fácil de configurar y utilizar. Puede iniciarse directamente desde la línea de comandos o integrarse en scripts de Python.
- Compatibilidad con FastAPI: Uvicorn es la opción recomendada para ejecutar aplicaciones creadas con FastAPI, un moderno framework web rápido para Python.

```bash
#para este caso usamos servidor con distribución expoencial sincrono.
uvicorn servidor_exp_time:app --host 0.0.0.0 --port 8001 --reload
```
Aquí, "servidor" es el nombre del archivo Python (sin la extensión .py) que contiene la aplicación FastAPI, y app es el nombre de la instancia de la aplicación dentro de ese archivo.

La implementación del servidor se realizó sobre una imagen de Docker, que es subida a DockerHub. De esta manera, todos pueden tener acceso y para funcionar es necesario modificar la linea de los deployments de Kubernetes que hace referencia a la imagen que selecciona para la creación del contenedor y la linea de comando CMD que se visualiza en el mismo archivo.

A continuación se muestra uno de los deployments utilizados y comentamos las lineas que deben ser modificadas.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: depokevina
spec:
  replicas: 1
  selector:
    matchLabels:
      role: php-kevin-a
  template:
    metadata:
      labels:
        role: php-kevin-a
    spec:
      nodeSelector:
        kubernetes.io/hostname: minikube-m02
      containers:
      - name: php-kevin
        image: bocha2002/servidor_exp_time:latest   ##ESTA LINEA SE DEBE MODIFICAR DE ACUERDO AL SERVIDOR
        imagePullPolicy: IfNotPresent        
        ports:
        - containerPort: 8000
        command: ["/bin/sh", "-c", "uvicorn servidor_exp_time:app --host 0.0.0.0 --port 8000"] ##ESTA LINEA SE DEBE MODIFICAR DE ACUERDO AL SERVIDOR
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: "password"
        resources:
          requests:
            memory: "64Mi"
            cpu: "200m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```