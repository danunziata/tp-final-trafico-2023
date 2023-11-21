
FROM haproxy:2.3  
RUN mkdir --parents /var/lib/haproxy && chown -R haproxy:haproxy /var/lib/haproxy  
RUN mkdir /run/haproxy  
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg 
