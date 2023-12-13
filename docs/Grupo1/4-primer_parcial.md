# Códigos realizados para la obtención de graficas

## Figura 4
```py
# Librerias a utilizar
import math                           #Para calcular el factorial de un nro
import matplotlib.pyplot as plt       #Para graficar los resultados obtenidos
from ipywidgets import interact
import ipywidgets as widgets

# FIGURE 4
# Parámetros del sistema
pm = list(range(2, 5 + 1, 1))                      # máquinas físicas
vm = 10                                            # máquinas virtuales (n)
cnt = list(range(1, 18 + 1, 1))                    # contenedores (k)
lambd = list(range(1000, 9982 + 1, 499))           # tasa de arribos al CDC
c = 300                                            # El número máximo de solicitudes de ejecución de tareas en la cola de LRS.
sobu = 0.0001                                      # 1/μ La duración del servicio de cada solicitud de ejecución de tareas en la cola del balanceador de carga.
sobu1 = 0.001                                      # 1/μ1 La duración promedio de servicio de cada tarea en la cola de LRS es de 0.001 segundos.
sobu2 = 0.01                                       # 1/μ2 Las duraciones de ejecución de tareas en los contenedores de cada MV son variables aleatorias exponenciales independientes e idénticamente distribuidas con una duración promedio de 0.01 segundos.
u = 1/sobu
u1 = 1/sobu1
u2 = 1/sobu2 
colores = ['b', 'g', 'r', 'c', 'm']                # Colores para graficar
response_data1 = []                                # Vectores para guardar los datos y graficar
response_data2 = []
response_data3 = []
response_data4 = []

# Variacion de las máquinas fisicas
for pim in pm:

    # Variacion del lambda
    for globalarribalrate in lambd:
        # LOAD BALANCER
        elb = globalarribalrate/(u-globalarribalrate)                                       # Numero medio de tareas
        tlb = elb/globalarribalrate                                                         # Tiempo medio de respuesta

        # LRS
        lambd1 = globalarribalrate/pim                                                      # lambda_1  tasa de arribo a las PM
        filrs = lambd1/u1                                                                   # Carga en el buffer
        pjlosslrs = lambd1 * ((1-filrs)/(1-pow(filrs,(c+1))))*pow(filrs,c)                  # Tareas perdidas
        djlrs = lambd1 * ((1-(filrs)**c)/(1-(filrs)**(c+1)))                                # Rendimiento 
        xjlrs = (filrs/(1-filrs))*((1-((c+1)*(filrs)**c)+c*filrs**(c+1))/(1-filrs**(c+1)))  # Tareas en la PM
        ljlrs = 1 - ((1-filrs)/(1-filrs**(c+1)))                                            # Tareas en servicio
        mjlrs = xjlrs - ljlrs                                                               # Tareas esperando en el buffer
        cpulrs = djlrs/u1                                                                   # Utilizacion del CPU
        wjlrs = mjlrs/lambd1                                                                # Tiempo de espera por tareas
        tjlrs = xjlrs/djlrs                                                                 # Tiempo de respuesta por tarea

        # CONTAINER
        lambd2 = lambd1/vm                                                                  # lambda_2 tasa de arribos a los contenedores
        ficnt = lambd2/u2                                                                   # Tasa de arribos
        sumatoria2 = 0
        for ki in cnt:                                                                      # Acumulamos los valores para obtener la sumatoria
            sumatoria = (ficnt**ki)/math.factorial(ki)
            sumatoria2 = sumatoria + sumatoria2
            
        pilosscnt = ((ficnt**ki)/math.factorial(ki))/sumatoria2                             # Probabilidad de perdida
        xicnt = ficnt*(1-pilosscnt)                                                         # Numero de tareas en la iesima VM
        ticnt = 1/u2                                                                        # Tiempo de respuesta en la iesima VM
        
        sysresponse = tlb + tjlrs + ticnt

        if  pim-1==1:
            response_data1.append(sysresponse)
        elif  pim-1==2:
            response_data2.append(sysresponse)
        elif  pim-1==3:
            response_data3.append(sysresponse)
        elif  pim-1==4:
            response_data4.append(sysresponse)   

plt.figure(figsize=(10, 6))
plt.plot(lambd, response_data1, label='20 VM')
plt.plot(lambd, response_data2, label='30 VM')
plt.plot(lambd, response_data3, label='40 VM')
plt.plot(lambd, response_data4, label='50 VM')
plt.xlabel('Tasa de arribos al CDC [tareas/s]')
plt.ylabel('Tiempo de respuesta del sistema [s]')
plt.title('Efecto de la tasa de arribos en el tiempo de respuesta')
plt.legend(loc='best')
plt.grid(True)
plt.show()
```

## Figura 5
```py
# Librerias a utilizar
import math                           #Para calcular el factorial de un nro
import matplotlib.pyplot as plt       #Para graficar los resultados obtenidos
from ipywidgets import interact
import ipywidgets as widgets

# FIGURE 5
# Parámetros del sistema
pm = list(range(2, 5 + 1, 1))                      # máquinas físicas
vm = 10                                            # máquinas virtuales (n)
cnt = list(range(1, 18 + 1, 1))                    # contenedores (k)
lambd = list(range(1000, 9982 + 1, 499))           # tasa de arribos al CDC
c = 300                                            # El número máximo de solicitudes de ejecución de tareas en la cola de LRS.
sobu = 0.0001                                      # 1/μ La duración del servicio de cada solicitud de ejecución de tareas en la cola del balanceador de carga.
sobu1 = 0.001                                      # 1/μ1 La duración promedio de servicio de cada tarea en la cola de LRS es de 0.001 segundos.
sobu2 = 0.01                                       # 1/μ2 Las duraciones de ejecución de tareas en los contenedores de cada MV son variables aleatorias exponenciales independientes e idénticamente distribuidas con una duración promedio de 0.01 segundos.
u = 1/sobu
u1 = 1/sobu1
u2 = 1/sobu2
colores = ['b', 'g', 'r', 'c', 'm']                # Colores para graficar
response_data1 = []                                # Vectores para guardar los datos y graficar
response_data2 = []
response_data3 = []
response_data4 = []

# Variacion de las máquinas fisicas
for pim in pm:

    # Variacion del lambda
    for globalarribalrate in lambd:
        
        # LOAD BALANCER
        elb = globalarribalrate/(u-globalarribalrate)                                         # Numero medio de tareas
        tlb = elb/globalarribalrate                                                           # Tiempo medio de respuesta

        # LRS
        lambd1 = globalarribalrate/pim                                                        # lambda_1  tasa de arribo a las PM
        filrs = lambd1/u1                                                                     # Carga en el buffer
        pjlosslrs =  ((1-filrs)*filrs**c)/(1-filrs**(c+1))                                    # Tareas perdidas
        djlrs = lambd1 * ((1-(filrs)**c)/(1-(filrs)**(c+1)))                                  # Rendimiento 
        xjlrs = (filrs/(1-filrs))*((1-((c+1)*(filrs)**c)+c*filrs**(c+1))/(1-(filrs**(c+1))))  # Tareas en la PM
        ljlrs = 1 - ((1-filrs)/(1-(filrs**(c+1))))                                            # Tareas en servicio
        mjlrs = xjlrs - ljlrs                                                                 # Tareas esperando en el buffer
        cpulrs = djlrs/u1                                                                     # Utilizacion del CPU
        wjlrs = mjlrs/lambd1                                                                  # Tiempo de espera por tareas
        tjlrs = xjlrs/djlrs                                                                   # Tiempo de respuesta por tarea
        
        # CONTAINER
        containers = 18
        lambd2 = lambd1/vm                                                                    # lambda_2 tasa de arribos a los contenedores
        ficnt = lambd2/u2                                                                     # Tasa de arribos
        numerator = (lambd2 ** containers) / math.factorial(containers)
        denominator = sum((lambd2 ** i) / math.factorial(i) for i in range(containers + 1))
        pilo= numerator / denominator
        xicnt = ficnt*(1-pilosscnt)                                                           # Numero de tareas en la iesima VM
        ticnt = 1/u2                                                                          # Tiempo de respuesta en la iesima VM
        ptotal = pilosscnt + pjlosslrs
        sysresponse = ptotal * globalarribalrate

        if  pim-1==1:
            response_data1.append(sysresponse)
        elif  pim-1==2:
            response_data2.append(sysresponse)
        elif  pim-1==3:
            response_data3.append(sysresponse)
        elif  pim-1==4:
            response_data4.append(sysresponse)   

plt.figure(figsize=(10, 6))
plt.plot(lambd, response_data1, label='20 VM')
plt.plot(lambd, response_data2, label='30 VM')
plt.plot(lambd, response_data3, label='40 VM')
plt.plot(lambd, response_data4, label='50 VM')
plt.xlabel('Tasa de arribos al CDC [tareas/segundo]')
plt.ylabel('Tareas perdidas en el sistema [tareas]')
plt.title('Efecto de la tasa de arribos en las perdidas')
plt.legend(loc='best')
plt.grid(True)
plt.show()
```

## Figura 6
```py
# Librerias a utilizar
import math                           #Para calcular el factorial de un nro
import matplotlib.pyplot as plt       #Para graficar los resultados obtenidos
from ipywidgets import interact
import ipywidgets as widgets

# FIGURE 6
# Parámetros del sistema
pm = list(range(2, 5 + 1, 1))                      # máquinas físicas
vm = 10                                            # máquinas virtuales (n)
cnt = list(range(1, 18 + 1, 1))                    # contenedores (k)
lambd = list(range(1000, 9982 + 1, 499))           # tasa de arribos al CDC
c = 300                                            # El número máximo de solicitudes de ejecución de tareas en la cola de LRS.
sobu = 0.0001                                      # 1/μ La duración del servicio de cada solicitud de ejecución de tareas en la cola del balanceador de carga.
sobu1 = 0.001                                      # 1/μ1 La duración promedio de servicio de cada tarea en la cola de LRS es de 0.001 segundos.
sobu2 = 0.01                                       # 1/μ2 Las duraciones de ejecución de tareas en los contenedores de cada MV son variables aleatorias exponenciales independientes e idénticamente distribuidas con una duración promedio de 0.01 segundos.
u = 1/sobu
u1 = 1/sobu1
u2 = 1/sobu2
colores = ['b', 'g', 'r', 'c', 'm']                # Colores para graficar
response_data1 = []                                # Vectores para guardar los datos y graficar
response_data2 = []
response_data3 = []
response_data4 = []

# Variacion de las máquinas fisicas
for pim in pm:

    # Variacion del lambda
    for globalarribalrate in lambd:
        
        # LOAD BALANCER
        elb = globalarribalrate/(u-globalarribalrate)                                         # Numero medio de tareas
        tlb = elb/globalarribalrate                                                           # Tiempo medio de respuesta

        # LRS
        lambd1 = globalarribalrate/pim                                                        # lambda_1  tasa de arribo a las PM
        filrs = lambd1/u1                                                                     # Carga en el buffer
        pjlosslrs = ((1-filrs)*filrs**c)/(1-filrs**(c+1))                                     # Tareas perdidas
        djlrs =  globalarribalrate * ((1-(filrs)**c)/(1-(filrs)**(c+1)))                      # Rendimiento 
        xjlrs = (filrs/(1-filrs))*((1-((c+1)*(filrs)**c)+c*filrs**(c+1))/(1-(filrs**(c+1))))  # Tareas en la PM
        ljlrs = 1 - ((1-filrs)/(1-(filrs**(c+1))))                                            # Tareas en servicio
        mjlrs = xjlrs - ljlrs                                                                 # Tareas esperando en el buffer
        cpulrs = djlrs/u1                                                                     # Utilizacion del CPU
        wjlrs = mjlrs/lambd1                                                                  # Tiempo de espera por tareas
        tjlrs = xjlrs/djlrs                                                                   # Tiempo de respuesta por tarea
        
        # CONTAINER
        lambd2 = lambd1/vm                                                                    # lambda_2 tasa de arribos a los contenedores
        ficnt = lambd2/u2                                                                     # Tasa de arribos
        sumatoria2 = (ficnt**18)/math.factorial(18)
        for ki in cnt:                                                                        # Acumulamos los valores para obtener la sumatoria
            sumatoria = (ficnt**ki)/math.factorial(ki)
            sumatoria2 = sumatoria + sumatoria2
            
        pilosscnt = ((ficnt**18)/(math.factorial(18)))/(sumatoria2)                           # Probabilidad de perdida
        
        xicnt = ficnt*(1-pilosscnt)                                                           # Numero de tareas en la iesima VM
        ticnt = 1/u2                                                                          # Tiempo de respuesta en la iesima VM
        
        sysresponse = djlrs

        if  pim-1==1:
            response_data1.append(sysresponse)
        elif  pim-1==2:
            response_data2.append(sysresponse)
        elif  pim-1==3:
            response_data3.append(sysresponse)
        elif  pim-1==4:
            response_data4.append(sysresponse)   

plt.figure(figsize=(10, 6))
plt.plot(lambd, response_data1, label='20 VM')
plt.plot(lambd, response_data2, label='30 VM')
plt.plot(lambd, response_data3, label='40 VM')
plt.plot(lambd, response_data4, label='50 VM')
plt.xlabel('Tasa de arribos al CDC [tareas/s]')
plt.ylabel('Tareas procesadas en el sistema [tareas/s]')
plt.title('Efecto de la tasa de arribos en el procesamiento del sistema')
plt.legend(loc='best')
plt.grid(True) 
plt.show()
```

## Figura 7
```py
# Librerias a utilizar
import math                           #Para calcular el factorial de un nro
import matplotlib.pyplot as plt       #Para graficar los resultados obtenidos
from ipywidgets import interact
import ipywidgets as widgets

# FIGURE 7
# Parámetros del sistema
pm = list(range(2, 5 + 1, 1))                      # máquinas físicas
vm = 10                                            # máquinas virtuales (n)
cnt = list(range(1, 18 + 1, 1))                    # contenedores (k)
lambd = list(range(1000, 9982 + 1, 499))           # tasa de arribos al CDC
c = 300                                            # El número máximo de solicitudes de ejecución de tareas en la cola de LRS.
sobu = 0.0001                                      # 1/μ La duración del servicio de cada solicitud de ejecución de tareas en la cola del balanceador de carga.
sobu1 = 0.001                                      # 1/μ1 La duración promedio de servicio de cada tarea en la cola de LRS es de 0.001 segundos.
sobu2 = 0.01                                       # 1/μ2 Las duraciones de ejecución de tareas en los contenedores de cada MV son variables aleatorias exponenciales independientes e idénticamente distribuidas con una duración promedio de 0.01 segundos.
u = 1/sobu
u1 = 1/sobu1
u2 = 1/sobu2
colores = ['b', 'g', 'r', 'c', 'm']                # Colores para graficar
response_data1 = []                                # Vectores para guardar los datos y graficar
response_data2 = []
response_data3 = []
response_data4 = []

# Variacion de las máquinas fisicas
for pim in pm:

    # Variacion del lambda
    for globalarribalrate in lambd:
        # c = pim * containers * 10
        # LOAD BALANCER
        elb = globalarribalrate/(u-globalarribalrate)                                         # Numero medio de tareas
        tlb = elb/globalarribalrate                                                           # Tiempo medio de respuesta

        # LRS
        lambd1 = globalarribalrate/pim                                                        # lambda_1  tasa de arribo a las PM
        filrs = lambd1/u1                                                                     # Carga en el buffer
        pjlosslrs = ((1-filrs)*filrs**c)/(1-filrs**(c+1))                                     # Tareas perdidas
        djlrs =  globalarribalrate * ((1-(filrs)**c)/(1-(filrs)**(c+1)))                      # Rendimiento 
        xjlrs = (filrs/(1-filrs))*((1-((c+1)*(filrs)**c)+c*filrs**(c+1))/(1-(filrs**(c+1))))  # Tareas en la PM
        ljlrs = 1 - ((1-filrs)/(1-(filrs**(c+1))))                                            # Tareas en servicio
        mjlrs = xjlrs - ljlrs                                                                 # Tareas en una maquina fisica
        cpulrs = djlrs/u1                                                                     # Utilizacion del CPU
        wjlrs = mjlrs/lambd1                                                                  # Tiempo de espera por tareas
        tjlrs = xjlrs/djlrs                                                                   # Tiempo de respuesta por tarea
        
        # CONTAINER
        lambd2 = lambd1/vm                                                                    # lambda_2 tasa de arribos a los contenedores
        ficnt = lambd2/u2                                                                     # Tasa de arribos
        sumatoria2 = (ficnt**18)/math.factorial(18)
        for ki in cnt:                                                                        # Acumulamos los valores para obtener la sumatoria
            sumatoria = (ficnt**ki)/math.factorial(ki)
            sumatoria2 = sumatoria + sumatoria2
            
        pilosscnt = ((ficnt**18)/(math.factorial(18)))/(sumatoria2)                           # Probabilidad de perdida
        
        xicnt = ficnt*(1-pilosscnt)                                                           # Numero de tareas en la iesima VM
        ticnt = 1/u2                                                                          # Tiempo de respuesta en la iesima VM
        ptotal = pilosscnt + pjlosslrs
        
        sysresponse =  mjlrs * pim + elb

        if  pim-1==1:
            response_data1.append(sysresponse)
        elif  pim-1==2:
            response_data2.append(sysresponse)
        elif  pim-1==3:
            response_data3.append(sysresponse)
        elif  pim-1==4:
            response_data4.append(sysresponse)   

plt.figure(figsize=(10, 6))
plt.plot(lambd, response_data1, label='20 VM')
plt.plot(lambd, response_data2, label='30 VM')
plt.plot(lambd, response_data3, label='40 VM')
plt.plot(lambd, response_data4, label='50 VM')
plt.xlabel('Tasa de arribos al CDC [tareas/s]')
plt.ylabel('Numero de tareas en el sistema [tareas]')
plt.title('Efecto de la tasa de arribos en las tareas')
plt.legend(loc='best')
plt.grid(True)
plt.show()
```

## Figura 8
```py
# Librerias a utilizar
import math                           #Para calcular el factorial de un nro
import matplotlib.pyplot as plt       #Para graficar los resultados obtenidos
from ipywidgets import interact
import ipywidgets as widgets

# FIGURE 8
# Parámetros del sistema
pm = list(range(2, 5 + 1, 1))                      # máquinas físicas
vm = 10                                            # máquinas virtuales (n)
cnt = list(range(1, 18 + 1, 1))                    # contenedores (k)
lambd = list(range(1000, 9982 + 1, 499))           # tasa de arribos al CDC
c = 300                                            # El número máximo de solicitudes de ejecución de tareas en la cola de LRS.
sobu = 0.0001                                      # 1/μ La duración del servicio de cada solicitud de ejecución de tareas en la cola del balanceador de carga.
sobu1 = 0.001                                      # 1/μ1 La duración promedio de servicio de cada tarea en la cola de LRS es de 0.001 segundos.
sobu2 = 0.01                                       # 1/μ2 Las duraciones de ejecución de tareas en los contenedores de cada MV son variables aleatorias exponenciales independientes e idénticamente distribuidas con una duración promedio de 0.01 segundos.
u = 1/sobu
u1 = 1/sobu1
u2 = 1/sobu2
colores = ['b', 'g', 'r', 'c', 'm']                # Colores para graficar
response_data1 = []                                # Vectores para guardar los datos y graficar
response_data2 = []
response_data3 = []
response_data4 = []

# Variacion de las máquinas fisicas
for pim in pm:

    # Variacion del lambda
    for globalarribalrate in lambd:
        # LOAD BALANCER
        elb = globalarribalrate/(u-globalarribalrate)                                       # Numero medio de tareas
        tlb = elb/globalarribalrate                                                         # Tiempo medio de respuesta

        # LRS
        lambd1 = globalarribalrate/pim                                                      # lambda_1  tasa de arribo a las PM
        filrs = lambd1/u1                                                                   # Carga en el buffer
        pjlosslrs = lambd1 * ((1-filrs)/(1-pow(filrs,(c+1))))*pow(filrs,c)                  # Tareas perdidas
        djlrs = lambd1 * ((1-(filrs)**c)/(1-(filrs)**(c+1)))                                # Rendimiento 
        xjlrs = (filrs/(1-filrs))*((1-((c+1)*(filrs)**c)+c*filrs**(c+1))/(1-filrs**(c+1)))  # Tareas en la PM
        ljlrs = 1 - ((1-filrs)/(1-filrs**(c+1)))                                            # Tareas en servicio
        mjlrs = xjlrs - ljlrs                                                               # Tareas esperando en el buffer
        cpulrs = djlrs/u1                                                                   # Utilizacion del CPU
        wjlrs = mjlrs/lambd1                                                                # Tiempo de espera por tareas
        tjlrs = xjlrs/djlrs                                                                 # Tiempo de respuesta por tarea

        # CONTAINER
        lambd2 = lambd1/vm                                                                  # lambda_2 tasa de arribos a los contenedores
        ficnt = lambd2/u2                                                                   # Tasa de arribos
        sumatoria2 = 1
        for ki in cnt:                                                                      # Acumulamos los valores para obtener la sumatoria
            sumatoria = (ficnt**ki)/math.factorial(ki)
            sumatoria2 = sumatoria + sumatoria2
            
        pilosscnt = ((ficnt**18)/math.factorial(18))/sumatoria2                             # Probabilidad de perdida
        xicnt = ficnt*(1-pilosscnt)                                                         # Numero de tareas en la iesima VM
        ticnt = 1/u2                                                                        # Tiempo de respuesta en la iesima VM
        
        sysresponse = (djlrs/u1)*100

        if  pim-1==1:
            response_data1.append(sysresponse)
        elif  pim-1==2:
            response_data2.append(sysresponse)
        elif  pim-1==3:
            response_data3.append(sysresponse)
        elif  pim-1==4:
            response_data4.append(sysresponse)   
plt.figure(figsize=(10, 6))
plt.plot(lambd, response_data1, label='20 VM')
plt.plot(lambd, response_data2, label='30 VM')
plt.plot(lambd, response_data3, label='40 VM')
plt.plot(lambd, response_data4, label='50 VM')
plt.xlabel('Tasa de arribos al CDC [tareas/s]')
plt.ylabel('Uso del CPU (%)')
plt.title('Efecto de la tasa de arribos en el uso del CPU')
plt.legend(loc='best')
plt.grid(True) 
plt.show()
```