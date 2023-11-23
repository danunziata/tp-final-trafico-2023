# Cliente - Servidor

El objetivo es desarrollar un modelo de colas M/M/1 donde el tiempo de interarribo y el largo de las tareas poseen distribucion exponencial. Se hizo uso de Locust como cliente generador de tráfico, mientras que el servidor es una aplicación creada con FastApi. Ver implementación en [README](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/README.md)

Para ello, se configuró tanto el cliente como servidor para que cumplan este requisito de la siguiente manera:

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
sudo apt-get install python3 --version 3.10.12
```
En caso de no tener el gestor de paquetes de python
```bash
sudo apt install python3-pip
```
A continuación se indica el siguiente comando utilizado para instalar locust
```bash
pip install locust --version 2.18.1
```
### Implementacion
Creando un archivo cliente Locust:
```bash
touch cliente.py
```
El codigo correspondiente al cliente (`cliente.py`), el cual se encuentra en el siguiente link de GitHub: [cliente.py](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/cliente.py)
```py
from locust import HttpUser, task
import time, random
```
Importa las clases y funciones necesarias de Locust, así como los módulos time y random.
```py
lambd = 1000
```
Establece la variable “lambd” en 1000. Esta variable se utiliza como parámetro para la función random.expovariate(lambd), que genera un número aleatorio distribuido exponencialmente con una tasa media de “lambd”.
```py
class HelloWorldUser(HttpUser):
    a = random.expovariate(lambd)
    wait_time = time.sleep(a)
```
Define una clase HelloWorldUser que hereda de la clase HttpUser de Locust. Esta clase representa un usuario que realizará solicitudes a la aplicación.

Genera un número aleatorio “a” distribuido exponencialmente con una tasa media de lambd utilizando random.expovariate(lambd).

Establece el tiempo de espera entre las solicitudes del usuario utilizando wait_time = time.sleep(a). Esto simula el tiempo que un usuario real podría esperar entre acciones.
```py
    @task
    def hello_world(self):
          self.client.get("")
```
Define un método hello_world decorado con “@task”, que indica que es una tarea que el usuario realizará. En este caso, la tarea consiste en realizar una solicitud HTTP GET a la ruta especificada por self.client.get("").

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
- Host: debemos ingresar la ip y puerto del servidor (en este caso es http://192.168.0.68:8001). Si se realiza de manera local, dejar este campo vacío.

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
pip install FastAPI --version 0.95.1
```

Luego, se necesita el servidor Uvicorn, por lo que se debe implementar la siguiente linea en el terminal:
```bash
pip install uvicorn --version 0.21.1
```
### Implementacion
El script que hace referencia a la aplicación realizada con FastApi es (`servidor.py`), el cual está en [servidor.py](https://github.com/danunziata/tp-final-trafico-2023/blob/main/code/GeneradorDeTrafico/servidor.py):
```py
from fastapi import FastAPI
import random, time
```

Importa la clase FastAPI del módulo fastapi.

Importa los módulos random y time para generar números aleatorios y pausar la ejecución, respectivamente.

```py
app = FastAPI()
```
Crea una instancia de la clase FastAPI. Esto representa la aplicación web que responderá a las solicitudes HTTP.
```py
mu = 100
```
Establece la variable mu en 100. Esta variable se usa como parámetro para la función “random.expovariate(mu)”, que genera un número aleatorio distribuido exponencialmente con una tasa media de “mu”.
```py
@app.get("/")
async def root():
    a = random.expovariate(mu)
    time.sleep(a)
    return {a}
```
Define una ruta para el método HTTP GET en la raíz ("/") de la aplicación.

La función root se ejecutará cuando se realice una solicitud HTTP GET a la ruta raíz.

Genera un número aleatorio “a” distribuido exponencialmente con una tasa media de mu utilizando random.expovariate(mu).

Pausa la ejecución del programa durante un tiempo dado por el valor de “a” utilizando “time.sleep(a)”. Esto simula algún tipo de operación que lleva un tiempo aleatorio.

Retorna un diccionario que contiene el valor de “a”. En este caso, el valor de a se incluye en un conjunto ({a}). Es importante señalar que, normalmente, en una API, se devolvería un objeto JSON más estructurado. En este caso, se está devolviendo un conjunto con un solo elemento.
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
