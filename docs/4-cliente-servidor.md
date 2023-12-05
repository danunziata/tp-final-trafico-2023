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

Por último, hicimos un script con un programa de python que no se ejecuta con el generador de tráfico Locust.

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
En cuanto al servidor, también hay dos programas. Uno con distribución uniforme asíncrono [servidor_unif_async.py](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/servidor_unif_async.py)
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
uvicorn servidor:app --host 0.0.0.0 --port 8001 --reload
```
Aquí, "servidor" es el nombre del archivo Python (sin la extensión .py) que contiene la aplicación FastAPI, y app es el nombre de la instancia de la aplicación dentro de ese archivo.
