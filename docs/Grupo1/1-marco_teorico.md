# Marco teórico
A continuación, se hará una descripción de los diferentes modelos que se realizarán en la implementación del clúster. Cabe aclarar que esta se basa en el esquema teórico presentado en el paper “Dynamic Scalability Model for Containerized Cloud Services” pero adaptada a la utilización de tecnologías específicas como Haproxy para el balanceo de carga o Kubernetes para gestionar los contenedores donde se ejecuta el servicio. También se explicarán las consideraciones que se toman para simplificar el modelo y las particularidades del escenario real en diferencia del ideal.

Primero, se realizó un codigo en Python para poder simular las mismas situaciones que se plantearon en el paper. Se encuentra en el siguiente link de GitHub: [Primer_parcial](https://github.com/danunziata/tp-final-trafico-2023/tree/locust/docs/Grupo1/4-primer_parcial.md)

Ahora, veremos las figuras obtenidas y analizaremos lo que se puede observar de ellas, comparandolas con las del paper.

#### Figura 4 (Nro. de figura correspondiente al paper)
![Efecto de la tasa de arribo en el tiempo de respuesta](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/img/figura4.jpg "Figura 4 - Paper de referencia")
Es evidente que a medida que aumenta la tasa de llegada global de tareas, el tiempo de respuesta aumenta. Además, se puede notar que para las cuatro configuraciones, el sistema en la nube no presenta un cambio radical cuando la tasa de llegada global de tareas se encuentra entre 5500 y 9500 tareas por segundo. Sin embargo, cuando superamos las 9500 tareas por segundo, el tiempo de respuesta del sistema cambia de manera exponencial para los cuatro casos, y a medida que disminuye el número de instancias de contenedores, el tiempo de respuesta del sistema aumenta y alcanza 0.4 segundos a una tasa de llegada global de 10000 tareas por segundo en el caso de la primera configuración.

#### Figura 5 
![Efecto de la tasa de arribo en las perdidas](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/img/figura5.jpg "Figura 5 - Paper de referencia")
La Figura 5 muestra la tasa de abandono del sistema, en la cual las tareas pueden ser rechazadas debido a la falta de capacidad en la plataforma del CDC o la falta de espacio en las colas de LRS. El conteo de tareas abandonadas sigue aumentando con el aumento de la tasa de llegada de tareas por segundo. Por lo tanto, si hay una carga excesiva, puede haber un retraso que provoca que algunas tareas sean abandonadas.  Es evidente que a medida que aumenta el número de instancias de contenedores, la tasa de abandono del sistema disminuye.

#### Figura 6 
![Efecto de la tasa de arribo en el procesamiento del sistema](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/img/figura6.jpg "Figura 6 - Paper de referencia")
La Figura 6 resume los resultados de nuestro modelo probado, informando sobre el rendimiento alcanzado en relación con la tasa de envío de tareas deseada, utilizando las cuatro configuraciones. El número de instancias de contenedores asignadas afecta el rendimiento del sistema.

#### Figura 7 
![Efecto de la tasa de arribo en las tareas](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/img/figura7.jpg "Figura 7 - Paper de referencia")
La Figura 7 muestra el efecto del número de instancias de contenedores en el número de tareas en el CDC cuando se varía la tasa global de llegada. Es evidente que cuando se trabaja con un mayor número de contenedores (la cuarta configuración) y la tasa de llegada global no supera las 5000 tareas por segundo, el CDC puede procesar más tareas, lo que permite reducir el número de tareas en el CDC. En el caso de que la tasa de llegada global supere las 5000 tareas por segundo, el CDC con un mayor número de contenedores presenta una gran cantidad de tareas en el CDC. Esto se explica en los resultados de la simulación obtenidos en las Figuras 5 y 8. Cuando la utilización de la CPU es igual al 100% y el CDC contiene el mayor número de contenedores, la tasa de abandono de tareas del CDC disminuye en comparación con el CDC con menos contenedores (otras configuraciones). Las mismas observaciones se aplican a las otras cuatro configuraciones.

#### Figura 8 
![Efecto de la tasa de arribo en el uso de CPU](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/img/figura8.jpg "Figura 8 - Paper de referencia")
Como podemos ver en la Figura 8, para una tasa de llegada global de más de 2000 tareas por segundo, puede notarse que cuando usamos la primera configuración, podemos tener una violación de los requisitos de SLA (Acuerdos de nivel de servicio). Por otro lado, para una tasa de llegada global de 2000 tareas por segundo y menos, y cuando tenemos la cuarta configuración, se garantiza el cumplimiento de los requisitos de SLA. Por lo tanto, el número de instancias de contenedores en el CDC tiene un impacto en la medida de la utilización de la CPU.

Una vez visto y analizado la situación propuesta por el paper, pasamos a nuestra implementación.
En la siguiente imagen se muestra el esquema completo del sistema a realizar donde pueden observarse los 3 subsistemas que componen el clúster:

![Esquema de implementación Práctica](img/Sin%20Flechas.png)

## Generador de tráfico
Para simular el tráfico se realizó un script en Python que permite seleccionar la cantidad de usuarios y la tasa de arribo de cada usuario en particular, es decir, que la tasa de arribo total es el producto entre ambos parámetros. 

Dada la lógica del generador, existe una particularidad a tener en cuenta: la tasa de arribo por usuario obtenida será menor a la seleccionada. Esto se da porque además de esperar el tiempo requerido por la función de variable de distribución exponencial también se incluye el tiempo de respuesta del servidor. Esto es que un usuario espera la respuesta del servidor para generar una nueva petición. Este efecto desaparece cuando el tiempo medio de interarribo por usuario es considerablemente más grande que el tiempo medio de respuesta del servidor.

## Balanceador de carga
En cuanto al balanceador de carga, en el paper está representado por un modelo M/M/1. La primera “M” corresponde al proceso de arribo, el cual es posible gobernar debido a que se puede regular el tiempo de interarribo en el programa de Python realizado en el cliente. Respecto de la segunda “M” define proceso de servicio, también con distribución exponencial, en la implementación a realizar no se tiene certeza sobre qué distribución se tiene, ya que depende del servicio de Haproxy en el cual nuestra capacidad de modificación es limitada. Se podría considerar determinístico, ya que la acción a realizar es prácticamente igual para todas las tareas, modifica el stack de protocolos (capa 2, capa 3 y capa 4) y redistribuye de manera equitativa entre todas las máquinas físicas mediante la aplicación del algoritmo de Round Robin, si se consideran pequeñas variaciones en este tiempo de servicio también podría modelarse con una distribución normal. En el caso de nuestra implementación solo se tiene una PM. Por último se considera que la cola de haproxy es suficientemente grande como para considerarla infinita a los fines del trabajo.

![Primer Modelo](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/img/Primer%20Modelo.png)

## Nodos
En esta etapa el proceso de arribo también se caracteriza con “M” donde la nueva tasa es igual a la tasa de arribo total dividida la cantidad de worker nodes. En cuanto al proceso de servicio, se tiene un caso similar al de haproxy donde es difícil determinar qué distribución gobierna este proceso. 

Por último es necesario hacer la aclaración de que al definir la capacidad del sistema “C” , Kubernetes no gestiona colas de tareas, por lo que a priori C=1. Si bien esto llevaría a un sistema a pura pérdida en cada nodo, en el comportamiento que se observa no existe pérdida. Esto es por la acción del protocolo TCP sobre el que se monta HTTP que al estar orientado a la conexión garantiza la transmisión de las tareas a costa de una latencia mayor. Esto lo logra con diferentes herramientas como el control de ventana y la retransmisión, pudiendo generar colas tanto en el cliente como en el host del servidor.

![Segundo Modelo](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/img/Segundo%20Modelo.png)

## Pods/Contenedores
En relación al modelo adoptado para los pods y contenedores, en nuestro esquema práctico se representa de igual manera que en el documento de referencia. La primera letra de la notación de Kendall, la “M”, es la tasa de arribo dada por el lambda del modelo anterior dividido el numero de contenedores, por lo que es posible gobernarla. Por otro lado, la letra siguiente es una “M” también, ya que depende de la tasa de servicio  en el programa realizado para el servidor con FastApi, por lo que también es posible modificarla. Con relacion a la cantidad de servidores, en este caso se tienen “k” de los mismos ya que depende del número de contenedores. La cuarta letra demuestra la capacidad del sistema y de igual manera que antes es “k”, generando un sistema a pura pérdida. Las tareas no se encolan, se pierden. Un contenedor puede atender solo una tarea.

![Tercer Modelo](https://github.com/danunziata/tp-final-trafico-2023/blob/main/docs/img/Tercer%20Modelo.png)

Con todos estos detalles en cuenta el sistema completo también puede modelarse como M/M/1 pero en este caso la tasa de servicio de todo el sistema será la de un pod en particular definida como 100 r/s por la cantidad de pods.