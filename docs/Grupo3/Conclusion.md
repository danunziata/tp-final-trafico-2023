## CONCLUSION DE LA EXPERIMENTACION


Durante el desarrollo de este proyecto, buscamos la  investigacion e implementacion de tecnologías fundamentales como Kubernetes, HAProxy y Docker. Enfrentamos varios desafíos, algunos que pudimos abordar de manera efectiva y otros no debido a la falta de tiempo para terminar el proyecto.

Uno de los problemas mas relevantes que pudimos salvar fue de infrastructura.
 Al descubrir un puente entre los pods, esto se resolvio mediante la creación de servicios distintos y su asignación a nodos específicos.

En cuento a los que no pudimos solventar surgió en el ámbito del balanceo de carga. Inicialmente, la configuración "round robin" en HAProxy funcionaba de manera eficiente, garantizando la distribución equitativa de solicitudes entre los nodos. La hipotesis que sostenemos es que fue debido a la introducción del generador de tráfico con tiempos de interarribo asincrónicos lo cual generó complicaciones en la carga distribuida generando que no se respete su configuracion asignada, esto se debe a que en situaciones asincrónicas, existía la posibilidad de que algunas solicitudes se generaran y enviaran más rápidamente que otras. Si alguna solicitud se bloqueó o experimentó retrasos significativos, esto pudo haber afectado el equilibrio de carga.
Este problema podria haberse solventarse cambiando aspectos de configuracion de haproxy o cambiando ese aspecto del codigo del generador de trafico, sin embargo debido a la falta de tiempo eso no pudo lograrse.

Finalmente, algunos aspectos que pudimos observar fueron los siguientes:
Los sockets tcp que se generaban, no iban directamente de cliente a servidor, sino que se creaba un socket desde cliente a haproxy y luego desde haproxy a servidor.
Ademas ellos tenian una conexion persistente ya que se cerraban una vez cortada la ejecucion del programa que generaba trafico.
Otro aspecto fundamental, fue que no encontramos perdidas de solicitudes, ya que en diversas pruebas las solicitudes enviadas siempre  era igual a las solicitudes que recibiamos.
Por lo tanto descartamos que se pudiera modelar ese esquema como "MMKK" o a pura perdida.
La hipotesis que sostenemos respecto a esto, es que quien esta evitando esto es TCP ya que tiene mecanismos como ventaneo o control de flujo que permiten evitar la perdida de solicitudes.
Por ultimo con respecto a los tiempos que analizamos, 
por un lado los resultados variaban en un principio en funcion de los recursos de la computadora donde generabamos la infraestructura, por otro lado pese a ser distintos se aproximan bastante a lo que nos devolvia la aplicacion. Ademas pudimos observar claramente la divergencia teorica cuando tomabamos una carga de trabajo &rho; mayor que uno, lo cual implicaba saturacion.
Para culminar con esto, queremos agregar que pese a todas las dificultades del trabajo,  creemos que fue muy importante como parte de nuestro desarrollo como ingenieros aprender a armar un proyecto y enfrentarnos con todo los desafios que supone. 

