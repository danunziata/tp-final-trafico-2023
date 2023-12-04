# Implementación del esquema cliente-servidor Locust y FastApi

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
Creando un archivo cliente Locust:
```bash
touch cliente.py
```
El codigo correspondiente al cliente (`cliente.py`), el cual se encuentra en el siguiente link de GitHub: [cliente.py](agregar dir)
```py
from locust import HttpUser, task, between
import random
lambd=1000
class HelloWorldUser(HttpUser):

    @task
    def hello_world(self):
        self.client.get("")
```

## Servidor

El script que hace referencia a la aplicación realizada con FastApi es (`servidor.py`), el cual está en [servidor.py](agregar):
```py
from fastapi import FastAPI
import random
import asyncio

app = FastAPI()
mu = 100    # 1 / media

@app.get("/")
async def root():
    a=random.expovariate(mu)
    asyncio.sleep(a)
    return {1}
```

## Ejecución
Una vez creado los programas tanto para el cliente como el servidor, para ejecutar es necesario utilizar el servidor Uvicorn para levantar la aplicación creada con FastApi.

```bash
uvicorn servidor:app --host 0.0.0.0 --port 8001 --reload
```
En caso de estar el puerto ocupado, se puede ver lo siguiente:
```bash
Ss -ltn | grep "numero de puerto"
```

En cuanto al generador de tráfico, para ejecutarlo debemos estar situados en el directorio donde se encuentre el archivo cliente.py. Una vez allí, implementamos el siguiente comando:

```bash
locust -f “nombre del archivo.py”
```

Una vez iniciado eso, ir a la dirección que te aparece, por ejemplo
Starting web interface at http://0.0.0.0:8089 (accepting connections from all network interfaces)

Cuando ingresamos a esa dirección, deberíamos de ver la interfaz de locust donde podemos comenzar un nuevo test y debemos ingresar 3 parámetros:

- número de usuarios: Es el número máximo de usuarios al mismo tiempo en el sistema.
- Spawn rate:  Cantidad de usuarios que aparecen por segundo (dado que el código del cliente tiene una aparición exponencial hace que no sea de manera lineal)
- Host: debemos ingresar la ip y puerto del servidor (en este caso es http://192.168.0.68:8001). Si se realiza de manera local, dejar este campo vacío.
