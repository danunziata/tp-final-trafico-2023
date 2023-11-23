# Load Balancer
Load Balancer:

Es un concepto utilizado en la adminstración de sistemas informaticos que se refiere a la técnica de
repartir un conjunto de peticiones en un conjunto de ordenadores, procesadores u otros recursos.

Existen varios algoritmos que se encargan de determinar la manera en la que se reparten los mensajes.
En nuestro caso, decidimos utilizar Round-Robin. El mismo opera de la siguiente manera:
distribuye de forma equitativa los mensajes, hacia los servidores, otorgandole la misma prioridad. 

A la hora de diseñar un LoadBalancer, el software que utilizamos es Ha-Proxy. Es un software de código 
abierto que proporciona un equilibrador de carga de alta disponibilidad, que distribuye solicitudes entre
muchos servidores. 
