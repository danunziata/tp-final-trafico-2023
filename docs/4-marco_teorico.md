# Marco teórico
A continuación, se hará una descripción de los diferentes modelos que se realizarán en la implementación del clúster. Cabe aclarar que esta se basa en el esquema teórico presentado en el paper “Dynamic Scalability Model for Containerized Cloud Services” pero adaptada a la utilización de tecnologías específicas como Haproxy para el balanceo de carga o Kubernetes para gestionar los contenedores donde se ejecuta el servicio. También se explicarán las consideraciones que se toman para simplificar el modelo y las particularidades del escenario real en diferencia del ideal.

En la siguiente imagen se muestra el esquema completo de la implementación a realizar donde pueden observarse los 3 subsistemas que componen el clúster:

![Esquema de implementación Práctica](images/Sin%20Flechas.png)

## Generador de tráfico
Para simular el tráfico se realizó un script en Python que permite seleccionar la cantidad de usuarios y la tasa de arribo de cada usuario en particular, es decir, que la tasa de arribo total es el producto entre ambos parámetros. Dada la lógica del generador, existe una particularidad a tener en cuenta: la tasa de arribo por usuario obtenida será menor a la seleccionada. Esto se da porque además de esperar el tiempo requerido por la función de variable de distribución exponencial también se incluye el tiempo de respuesta del servidor, esto es que un usuario espera la respuesta del servidor para generar una nueva petición. Este efecto desaparece cuando el tiempo medio de interarribo por usuario es considerablemente más grande que el tiempo medio de respuesta del servidor.

## Balanceador de carga
En cuanto al balanceador de carga, en el paper está representado por un modelo M/M/1. La primera “M” corresponde al proceso de arribo, el cual es posible gobernar debido a que se puede regular el tiempo de interarribo en el programa de Python realizado en el cliente. Respecto de la segunda “M” define proceso de servicio, también con distribución exponencial, en la implementación a realizar no se tiene certeza sobre qué distribución se tiene, ya que depende del servicio de Haproxy en el cual nuestra capacidad de modificación es limitada. Se podría considerar determinístico, ya que la acción a realizar es prácticamente igual para todas las tareas, modifica el stack de protocolos (capa 2, capa 3 y capa 4) y redistribuye de manera equitativa entre todas las máquinas físicas mediante la aplicación del algoritmo de Round Robin, si se consideran pequeñas variaciones en este tiempo de servicio también podría modelarse con una distribución normal. En el caso de nuestra implementación solo se tiene una PM. Por último se considera que la cola de haproxy es suficientemente grande como para considerarla infinita a los fines del trabajo.

![Primer Modelo](images/Primer%20Modelo.png)

o esta

![Primer Modelo](https://github.com/danunziata/tp-final-trafico-2023/blob/main/images/Primer%20Modelo.png)

## Nodos
En esta etapa el proceso de arribo también se caracteriza con “M” donde la nueva tasa es igual a la tasa de arribo total dividida la cantidad de worker nodes, en cuanto al proceso de servicio se tiene  un caso similar al de haproxy donde es difícil determinar qué distribución gobierna este proceso. Por último es necesario hacer la aclaración de que al definir la capacidad del sistema “C” , kubernetes no gestiona colas de tareas, por lo que a priori C=1, si bien esto llevaría a un sistema a pura pérdida en cada nodo, en el comportamiento que se observa no existe pérdida. Esto es por la acción del protocolo TCP sobre el que se monta HTTP que al estar orientado a la conexión garantiza la transmisión de las tareas a costa de una latencia mayor. Esto lo logra con diferentes herramientas como el control de ventana y la retransmisión, pudiendo generar colas tanto en el cliente como en el host del servidor.

![Segundo Modelo][def]

## Pods/Contenedores
En relación al modelo adoptado para los pods y contenedores, en nuestro esquema práctico se representa de igual manera que en el documento de referencia. La primera letra de la notación de Kendall, la “M”, es la tasa de arribo dada por el lambda del modelo anterior dividido el numero de contenedores, por lo que es posible gobernarla. Por otro lado, la letra siguiente es una “M” también, ya que depende de la tasa de servicio  en el programa realizado para el servidor con FastApi, por lo que también es posible modificarla. Con relacion a la cantidad de servidores, en este caso se tienen “k” de los mismos ya que depende del número de contenedores. La cuarta letra demuestra la capacidad del sistema y de igual manera que antes es “k”, generando un sistema a pura pérdida. Las tareas no se encolan, se pierden. Un contenedor puede atender solo una tarea.

![Tercer Modelo](https://github.com/danunziata/tp-final-trafico-2023/blob/main/images/Tercer%20Modelo.png)

Con todos estos detalles en cuenta el sistema completo también puede modelarse como M/M/1 pero en este caso la tasa de servicio de todo el sistema será la de un pod en particular definida como 100 r/s por la cantidad de pods.