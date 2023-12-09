# Implementación del esquema cliente-servidor Locust y FastApi
En este Readme se encuentra la implementación básica del trabajo que se realizó. Para un enfoque más detallado, puede visitar [Cliente-Servidor](https://danunziata.github.io/tp-final-trafico-2023/4-cliente-servidor/)

## Instalación de Locust
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
## Instalación de FastApi
En primer lugar se debe instalar FastApi con el siguiente comando:
```bash
pip install FastAPI
```

Luego, se necesita el servidor Uvicorn, por lo que se debe implementar la siguiente linea en el terminal:
```bash
pip install uvicorn
```

Una vez instalado todo lo que se menciona arriba, necesitamos desarrollar los script para la aplicación del servidor con FastApi y el generador de tráfico con Locust.

## Cliente
Para realizar el script del cliente, primero realizamos uno con distribución exponencial de los tiempos de interarribo utilizando la librería de "time" por lo que era síncrona y se debía esperar la respuesta para enviar una nueva tarea. Se encuentra en el siguiente link de GitHub: [cliente_exp_time.py](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/cliente_exp_time.py)
```py
from locust import HttpUser, task, between
import time, random```
lambd=1000
class HelloWorldUser(HttpUser):
   
	@task
	def hello_world(self):
		a=random.expovariate(lambd)
		time.sleep(a)
		self.client.get("/")

```
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
Debido a los problemas que se han tenido con este generador de tráfico, se ha utilizado como cliente y generador de tráfico al archivo de python que se muestra en el siguiente enlace:  [Cliente_Final](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/Cliente_Final.py)

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

## Servidor
En cuanto al servidor, también hay tres programas. Uno con distribución uniforme asíncrono [servidor_unif_async.py](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/servidor_unif_async.py)
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

## Ejecución
Una vez creado los programas tanto para el cliente como el servidor, para ejecutar es necesario utilizar el servidor Uvicorn para levantar la aplicación creada con FastApi.

```bash
#En este caso usamos el servidor con distribución exponencial síncrono.
uvicorn servidor_exp_time:app --host 0.0.0.0 --port 8001 --reload
```
En caso de estar el puerto ocupado, se puede ver lo siguiente:
```bash
Ss -ltn | grep "numero de puerto"
```
La implementación del servidor se realizó sobre una imagen de Docker, que es subida a DockerHub. De esta manera, todos pueden tener acceso y para funcionar es necesario modificar la linea de los deployments de Kubernetes que hace referencia a la imagen que selecciona para la creación del contenedor y la linea de comando CMD que se visualiza en el mismo archivo.

En cuanto al generador de tráfico, para ejecutarlo debemos estar situados en el directorio donde se encuentre el archivo cliente.py. Una vez allí, implementamos el siguiente comando:

```bash
locust -f “nombre del archivo.py”
```

Una vez iniciado eso, ir a la dirección que te aparece, por ejemplo
Starting web interface at http://0.0.0.0:8089 (accepting connections from all network interfaces)

Cuando ingresamos a esa dirección, deberíamos de ver la interfaz de locust donde podemos comenzar un nuevo test y debemos ingresar 3 parámetros:

- número de usuarios: Es el número máximo de usuarios al mismo tiempo en el sistema.
- Spawn rate:  Cantidad de usuarios que aparecen por segundo (dado que el código del cliente tiene una aparición exponencial hace que no sea de manera lineal)
- Host: debemos ingresar la ip y puerto del servidor (en este caso es http://192.168.1.199:2023). Si se realiza de manera local, dejar este campo vacío.