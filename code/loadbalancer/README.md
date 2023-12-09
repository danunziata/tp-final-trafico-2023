# Balanceador de carga HA-Proxy sobre servicios de Kubernetes

La funcion de la utilizacion de esta aplicacion es levantar un balanceador de carga y luego mediante su archivo de configuracion correspondiente, establecer un sistema que distribuya uniformemente las peticiones
entrantes hacia los servidores. Esto se logra mediante el tipo de balanceo que se le asigna llamado "roundrobin"
A continuacion generamos dos implementaciones:

##implementacion1: esta es  para realizar el escenario final en la maquina fisica, con la aplicacion descargada sobre la misma 
##implementacion2: esta es una opcion util para poder implentarlo en docker si a si lo requieren en el futuro.

## Implementacion1:


En esta implementacion, vamos a explicar como configurar Ha-proxy para que apunten a dos servicios diferentes de kubernetes: uno con la aplicacion apache y el otro con la aplicacion nginix, estos servicios se van a colocar en en un solo nodo (maquina virtual) ya que 
tiene como finalidad probar en el balanceo entre ellos.

IMPORTANTE, para la implementacion final, deberan asociar cada servicio a un nodo en especifico. Esto se detalla en la rama de minikube, en donde tambien se brindan los archivos finales correspondientes.
La razon porque vamos a balancear entre servicios es porque queremos generar dos conjuntos de pods independientes entre si.


En primer lugar generamos el nodo de kubernetes en una maquina virtual con el siguiente comando:

 $minikube start --driver=virtualbox --nodes 1
 
Para poder chequear si esta listo para su utilizacion, con el siguiente comando verificamos que este en estado "ready"
 
 $kubectl get nodes 

Si no reconoce kubectl, podemos descarlo aplicando el comando que sugiere el error que nos da.
Una vez que verificamos que esta en ready, levantamos los dos deployment

 $kubectl apply -f d1.yaml IMPORTANTE, debemos estar parados en la carpeta donde estan todos los archivo. 
 $kubectl apply -f d2.yaml 

Estos dos deployment, estan configurados para generar dos pods, esto puede modificarse aplicando el comando nano y modificando el numero de replicas
 $sudo nano d1.yaml 

	apiVersion: apps/v1
	kind: Deployment
	metadata:
	  name: apachedep
	spec:
	  replicas: 2 #numero de pods
	  selector:
	    matchLabels:
	      app: apache
	  template:
	    metadata:
	      labels:
		app: apache  #etiqueta de los pods
	    spec:
	      containers:
	      - name: apachecont
		image: httpd:2.4 
		ports:
	


IMPORTANTE, luego de realizar cualquier configuracion, se debe utilizar el comando para levantar dicho deployment asi se aplican las actualizaciones

Luego, levantamos los servicios del tipo NODE PORT, para que nos genere un puerto externo el cual utilizaremos para poder acceder a ellos desde fuera de kubernetes.
Cada uno de ellos se vincula con su deployment correspondiente.
	
apiVersion: v1
kind: Service
metadata:
  name: apacheser  # nombre del servicio
spec:
  selector:
    app: apache  # etiquetado de los pods de deployment que quiero asociar
    node: minikube  # selector de nodo específico
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30000  # puerto externo
  type: NodePort  # tipo de servicio



 $kubectl apply -f s1.yaml IMPORTANTE, debemos estar parados en la carpeta donde estan todos los archivo. 
 $kubectl apply -f s2.yaml 


Finalmente, verificamos el estado de los servicios con el siguiente comando
 
 $kubectl get services, alli podemos ver la asignacion de puertos que se le hizo a cada servicio, debemos ver el primero con puerto "30000" y el segundo
 con puerto "30001". Cada servicio tiene un puerto diferente.

Luego averiguamos la ip del nodo en el que hicimos las configuaciones
 
 $kubectl get nodes -o wide

Ademas de esto, podemos verificar los pods que se asignaron a cada uno de los servicios con el siguiente comando

 $kubectl describe service <nombre-del-servicio>

Descargamos la aplicacion Ha-proxy
 $sudo apt update
 $sudo apt install haproxy

Finalmente entramos a configurar el "Ha-Proxy", para ello nos situamos en la siguiente carpeta:

 $cd /etc/haproxy

desde alli, entramos al archivo de configuracion "haproxy.cfg"

 $sudo nano haproxy.cfg



Al final de dicho archivo, luego de los "error file" sin modificar todo lo que esta previamente,  agregamos lo siguiente: 


######NO SE TOCA ESTO########

global
	log /dev/log	local0
	log /dev/log	local1 notice
	chroot /var/lib/haproxy
	stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
	stats timeout 30s
	user haproxy
	group haproxy
	daemon

	# Default SSL material locations
	ca-base /etc/ssl/certs
	crt-base /etc/ssl/private

	# See: https://ssl-config.mozilla.org/#server=haproxy&server-version=2.0.3&config=intermediate
        ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384
        ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
        ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

defaults
	log	global
	mode	http
	option	httplog
	option	dontlognull
        timeout connect 5000
        timeout client  50000
        timeout server  50000
	errorfile 400 /etc/haproxy/errors/400.http
	errorfile 403 /etc/haproxy/errors/403.http
	errorfile 408 /etc/haproxy/errors/408.http
	errorfile 500 /etc/haproxy/errors/500.http
	errorfile 502 /etc/haproxy/errors/502.http
	errorfile 503 /etc/haproxy/errors/503.http
	errorfile 504 /etc/haproxy/errors/504.http

######Agregamos a continuacion los frontend y backend######

#frontend : Se crean dos frontends:  
#__http_web__ : Se establece el funcionamiento de la entrada al balanceador de carga. Se asocia el puerto __:2023__ para recibir peticiones y dichas peticiones se repartiran en el backend llamado __milu__.  
#__stats__ : Se establece un frontend para visualizar las estadisticas del balanceador. Se asocia el puerto __:8404__ para visualizar, ademas se establecen los tiempos de actualizacion y se habilitan las estadisticas.  

#backend : Se crea el backend que contiene los servidores a los cuales enviaremos las peticiones recibidas del frontend utilizando el protocolo HTTP, y el algoritmo de balanceo _
 
 frontend http_web #para hacer el balanceo entre servidores
            bind IP_ASOCIADA_INTERFAZ_CABLEADA:2023 #en esta direccion escucha mi aplicacion haproxy
            mode http
            use_backend milu

    frontend stats #para ver las metricas de haproxy
        bind IP_DE_ALGUNA_INTERFAZ_DEL_HOST:8404
        mode http
        stats enable
        stats uri /haproxy-stats  
        stats refresh 10s

 
    backend milu
        mode http
        balance roundrobin
        option forwardfor
	http-response set-header X-Backend-Service %[srv_id]
        server serv1 IP_DEL_NODO:30000 #backends entre los que se va a balancear
        server serv2 IP_DEL_NODO:30001

a continuacion, aplicamos la configuracion con el siguiente comando:
  
 $service haproxy restart

Luego de todo esto, realizamos las pruebas pertinentes para corroborar su funcionamiento.

 $curl IP_DE_ALGUNA_INTERFAZ_DEL_HOST:2023 con este comando, al ejecutarlo varias veces vemos como alterna la respuesta entre un servicio y el otro

Para tener mas certeza de que servicio esta respondiendo, ya que deberemos implementar todo esto con la misma aplicacion, utilizamos el siguiente comando

 $curl -I IP_DE_ALGUNA_INTERFAZ_DEL_HOST:2023  con este comando veremos especificamente que servicio nos responde.

Para analizar las estadisticas, se puede utilizar la siguiente direccion:

> http://[IP_DONDE_ESCUCHA_HA-Proxy]:8404/haproxy-stats



## Implementacion2:

Crear un archivo ***Dockerfile*** con la siguiente configuracion:

    FROM haproxy:2.3  
    RUN mkdir --parents /var/lib/haproxy && chown -R haproxy:haproxy /var/lib/haproxy  
    RUN mkdir /run/haproxy  
    COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg  

Para este archivo, se utiliza la imagen de HA-Proxy 2.3, basada en Linux Alpine.  
Se deben crear los dos directorios dentro del docker para que HA-Proxy pueda copiar y utilizar su configuracion. Esto se hace con los dos renglones siguientes. Ademas se agregan permisos de lectura mediante el comando __chown -R__. Por ultimo, se copia el archivo que contiene la configuracion de HA-Proxy __haproxy.cfg__ dentro de los directorios creados anteriormente en el contenedor.

Crear un archivo ***haconfig.cfg*** con la siguiente configuracion:

    global
        log /dev/log	local0
        log /dev/log	local1 notice
        chroot /var/lib/haproxy
        stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
        stats timeout 30s
        user haproxy
        group haproxy
        daemon

        # Default SSL material locations
        ca-base /etc/ssl/certs
        crt-base /etc/ssl/private

        # See: https://ssl-config.mozilla.org/#server=haproxy&server-version=2.0.3&config=intermediate
            ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384
            ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
            ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

    defaults
        log	global
        mode	http
        option	httplog
        option	dontlognull
            timeout connect 5000
            timeout client  50000
            timeout server  50000

    frontend http_web
            bind *:2023
            mode http
            use_backend milu

    frontend stats
        bind *:8404
        mode http
        stats enable
        stats uri /haproxy-stats  
        stats refresh 10s

    backend milu
            mode http
            balance roundrobin
            option forwardfor
            server apache1 172.17.0.4:80 check
            server apache2 172.17.0.5:80 check

En este archivo se detalla toda la configuracion del balanceador de carga. 

    global
        log /dev/log	local0
        log /dev/log	local1 notice
        chroot /var/lib/haproxy
        stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
        stats timeout 30s
        user haproxy
        group haproxy
        daemon

***global*** : En esta seccion se detallan las configuraciones globales de HA-Proxy. Aqui se detalla informacion como por ejemplo el directorio raiz que utiliza HA-Proxy dentro del contenedor. Ademas se crea un socket para que HA-Proxy pueda mostrar las estadisticas y se establece que la aplicacion correra en segundo plano (daemon).

        # Default SSL material locations
        ca-base /etc/ssl/certs
        crt-base /etc/ssl/private

        # See: https://ssl-config.mozilla.org/#server=haproxy&server-version=2.0.3&config=intermediate
            ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384
            ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
            ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

***SSL*** : Se establece la ubicacion predeterminada para los archivos SSL

    defaults
        log	global
        mode	http
        option	httplog
        option	dontlognull
            timeout connect 5000
            timeout client  50000
            timeout server  50000

***defaults*** : Se configuran las opciones predeterminadas tanto para Backend como para Frontend (Entradas y Salidas del balanceador). Aqui se establece que se utiliza el protocolo HTTP y se descartan las conexiones que no transmiten datos. Ademas se establecen los timeout para conexiones, cliente y servidor.            

    frontend http_web
            bind *:2023
            mode http
            use_backend milu

    frontend stats
        bind *:8404
        mode http
        stats enable
        stats uri /haproxy-stats  
        stats refresh 10s

***frontend*** : Se crean dos frontends:  
__http_web__ : Se establece el funcionamiento de la entrada al balanceador de carga. Se asocia el puerto __:2023__ para recibir peticiones y dichas peticiones se repartiran en el backend llamado __milu__.  
__stats__ : Se establece un frontend para visualizar las estadisticas del balanceador. Se asocia el puerto __:8404__ para visualizar, ademas se establecen los tiempos de actualizacion y se habilitan las estadisticas.
  
    backend milu
        mode http
        balance roundrobin
        option forwardfor
        server apache1 172.17.0.4:80 check
        server apache2 172.17.0.5:80 check


***backend*** : Se crea el backend que contiene los servidores a los cuales enviaremos las peticiones recibidas del frontend utilizando el protocolo HTTP, y el algoritmo de balanceo __round robin__ y se agrega la direccion del cliente en la cabecera HTTP. Por ultimo, se configuran cada uno de los servidores a utilizar. En este caso se utilizaron servidores __apache__ a modo de ejemplo, con sus respectivas direcciones IP y sus puertos asociados. Ademas mediante el __check__, HA-Proxy verifica la disponibilidad de dichos servidores.            

## Crear el contenedor HA-Proxy y ejecutar

Para crear el contenedor, utilizar la siguiente linea, situados en el mismo directorio en el que se encuentran los dos archivos creados anteriormente:

    $ docker build -t my-haproxy .

Una vez creado el contenedor, es posible verificar si la configuracion asignada al archivo __haproxy.cfg__ es correcta y no presenta errores en la sintaxis. Para ello se puede utilizar el comando:

    $ docker run -it --rm --name haproxy-syntax-check my-haproxy haproxy -c -f /usr/local/etc/haproxy/haproxy.cfg

Para ejecutar el contenedor de HA-Proxy con la configuracion correspondiente, ejecutar el siguiente comando:

    $ docker run -d --name my-running-haproxy --sysctl net.ipv4.ip_unprivileged_port_start=0 my-haproxy

Para probar utilizando un apache, se puede utilizar la siguiente linea:

    $ docker run -d -p 8081:80 --name apache1 httpd:2.4

Esta linea levanta un servidor de prueba __apache1__ con puerto __:8081__. Esta configuracion se debe agregar dentro del backend del archivo __haproxy.cfg__. Si se varios contenedores apache y se agregan dentro del archivo de configuracion, para probar el balanceador se puede utilizar el comando __curl__:

    $ curl [IP del contenedor de HA-Proxy]:2023

Respuestas obtenidas: (Se modifico el index.html de un apache para distinguir las respuestas)

    ➜  curl 172.17.0.5:2023
    <html><body><h1>It works!</h1></body></html>
    ➜  curl 172.17.0.5:2023
    <html><body><h1>It works!-------2</h1></body></html>

Para analizar las estadisticas, se puede utilizar la siguiente direccion:

> http://[IP del contenedor de HA-Proxy]:8404/haproxy-stats
