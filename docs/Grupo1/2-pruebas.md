
# Pruebas
En esta sección se presentan las pruebas realizadas durante el desarrollo de la implementación práctica para obtener conclusiones.

## Prueba 1
En la primera prueba se busca identificar cuantas peticiones por segundo puede manejar el servidor al variar el número de pods.

En la siguiente imagen se muestra el numero de paquetes por segundo en función del tiempo cuando varía la cantidad de pods que equivale a variar contenedores.

![Variacion_pods](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/Grupo1/img/Pruebas/variaciondepods2.png "Prueba de variación de pods")

Puede verse claramente que hay una relación lineal en el límite de request per second (rps) con el número de pods, siendo que se aumentaron en el siguiente orden: 2, 4, 6, 8.

Este comportamiento no debería sorprender si tenemos en cuenta que cada pod individualmente, gestiona de forma ideal 100 rps en promedio. Estos números no se logran ya que hay otros tiempos en juego en la implementación que disminuyen la performance del sistema. 

En base a los datos obtenidos se realiza una estimación de las rps promedio reales de un pod individualmente que oscilan entre 65 y 85 rps dependiendo de factores como las máquinas físicas donde se implementan, las conexiones utilizadas y otros.

Cabe aclarar que en todos los casos se aseguró que el servidor estuviera a máxima capacidad seleccionando correctamente el número de usuarios y sus respectivos "lambda" en el generador de tráfico.

## Prueba 2
En la segunda prueba el objetivo es realizar las comparación del tiempo de respuesta con el modelo teórico al variar el "ro" o `p`. 

Para hacer los cálculos fue necesario fijar la tasa de servicio, que se estimó con los datos de la prueba 1 en 75 rps por pod y, luego, se fijó la cantidad de pod en 2, por lo tanto el sistema podrá atender 150 rps aproximadamente.

### Caso 1
Si queremos obtener un `p` de 0.4 entonces la tasa de arribo total que debemos enviar es de = `p . mu`. Por lo tanto lambda es 60 1/s.

El tiempo medio de respuesta teórico en un sistema M/M/1 se puede calcular mediante la relación de 1/(mu - lambda).

Si `p = 0.4` deberíamos de obtener 11.11ms. Lo que se obtuvo en la práctica es:

![caso1](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/Grupo1/img/Pruebas/caso1.png)

### Caso 2
Para `p` de 0.6 entonces la tasa de arribo total que debemos enviar es 90 1/s.

En este caso deberíamos obtener 16.66 ms de retardo medio. Se llegó a lo siguiente:

![caso2](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/Grupo1/img/Pruebas/caso2.png)

### Caso 3
Para `p` de 0.8 entonces la tasa de arribo total que debemos enviar es 120 1/s.

En este caso deberíamos obtener 33.33 ms de retardo medio. Se llegó a lo siguiente:

![caso3](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/Grupo1/img/Pruebas/caso3.png)

### Caso 4
Para `p` de 0.9 entonces la tasa de arribo total que debemos enviar es 135 1/s.

En este caso deberíamos obtener 66.66 ms de retardo medio. Se llegó a lo siguiente:

![caso4](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/Grupo1/img/Pruebas/caso4.png)

### Caso 5
Para `p` de 0.99 la tasa de arribo total que debemos enviar es 148 1/s.

![caso6](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/Grupo1/img/Pruebas/caso6.png)

### Graficas 

La siguiente tabla nos muestra los valores de Tiempo medio de servicio reales e ideales correspondientes a distintos valores de ρ.

![tabla](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/Grupo1/img/Pruebas/tabla.png)

Con los valores anteriores se realizo la siguiente grafica para poder visualizar las diferencias entre la implementacion y los calculos teoricos.

![grafica](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/Grupo1/img/Pruebas/grafico.png)


### Caso de prueba teorico
Si `p > 1`, por ejemplo, que genere una tasa de arribo de 1000 tareas por segundo, las formulas teoricas no aplican y el modelo tendria un delay infinito.

![caso5](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/Grupo1/img/Pruebas/caso5.png)

En el caso de la implementacion real este fenomeno se observa en el hecho de que cuando se utiliza p > 1 el calculo de tiempo medio de respuesta del sistema no converge para ninguna cantidad x de paquetes incluidos en el calculo de la media, se presenta una tendencia de crecimiento hacia el "infinito", y la velocidad de esta esta determinada por que tanto supera p a 1, pero a fines practicos sabemos que existe algun limite ya sea por el hardware o por el timeout de TCP y partir de ese punto existira perdida de paquetes. Este analisis no esta considerado dentro de nuestro modelado.