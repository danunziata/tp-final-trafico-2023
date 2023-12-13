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
        #pass

    #La siguientes lineas hacen que el cliente espere la respuesta 
        data = await response.text()
        #print(f"Response from server: {data}")

    # Medir el tiempo después de recibir la respuesta y almacenar el tiempo de respuesta
    end_time = asyncio.get_event_loop().time()
    response_time = end_time - start_time
    response_times.append(response_time)
    #print(f"response time  {response_time}")

    # Mostrar el tiempo promedio cada 100 paquetes
    if len(response_times) % 100 == 0:
        average_response_time = sum(response_times) / len(response_times)
        #print(f" Tiempo medio de servicio luego de enviar {len(response_times)} paquetes: {average_response_time} segundos")

async def generate_traffic(user_id, session, host, port, path, lambda_value):
    while True:
        # Esperar un tiempo según la distribución exponencial antes de comenzar
        inter_arrival_time = random.expovariate(lambda_value)
        #print(f"User {user_id}: Will wait for {inter_arrival_time} seconds before starting")

        await asyncio.sleep(inter_arrival_time)

        # Ejecutar la solicitud
        await send_request(session, host, port, path, user_id)

async def main():
    host = "192.168.100.31"
    port = 2023  # Reemplaza con el puerto correcto
    path = "/"  # Reemplaza con la ruta correcta

    num_users = int(input("Ingrese la cantidad de usuarios: "))
    lambda_value = float(input("Ingrese el valor de lambda para la distribución exponencial: "))

    # Configurar el límite de conexiones
    connector = aiohttp.TCPConnector(limit=num_users)

    async with aiohttp.ClientSession(connector=connector) as session:
        user_tasks = [generate_traffic(user_id, session, host, port, path, lambda_value) for user_id in range(1, num_users + 1)]
        await asyncio.gather(*user_tasks)

if __name__ == "__main__":
    asyncio.run(main())
