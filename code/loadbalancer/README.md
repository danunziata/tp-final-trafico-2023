# Balanceador de carga HA-Proxy

La funcion del siguiente contenedor es levantar un balanceador de carga con HA-Proxy y luego mediante su archivo de configuracion correspondiente, establecer un sistema que distribuya uniformemente las peticiones
entrantes hacia los servidores.

## Implementacion:

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
