# U01_DS_NetworkingSockets

## Explicación

La conexión se realiza mediante sockets en protocolo de comunicación TCP.

- El agente que solicita la ayuda juega el papel de servidor.
- Los agentes que aceptan o rechazan ayudar juegan el papel de clientes.

Para poner a prueba el programa, es necesario:
- Iniciar el servidor ejecutando una instancia de ```server.py```.
- Iniciar los clientes ejecutando tres instancias de ```client.py```.

Se recomienda hacerlo en cuatro terminales aparte para separar la impresión de mensajes por pantalla.

## Requisitos

Para desarrollar este programa se ha utilizado:
- ```Python 3.10.7```.
- ```socket```: comunicación en el lado del cliente.
- ```socketserver```: comunicación en el lado del servidor.
- ```pickle```: serialización de objetos.
- ```datetime```: obtención de estampas de tiempo y operaciones con ```timedeltas```.
- ```random```: generación de números aleatorios, gestión de probabilidad y tiempos de espera.
- ```time```: utilización de la función ```sleep```.
- ```threading```: utilización de primitivas de control de la concurrencia, como ```Lock``` y ```Barrier```.

## Consideraciones

- En los archivos se incluyen constantes que pueden ser modificadas a conveniencia del usuario para probar diferentes condiciones.
- La librería ```message.py``` contiene una estructura de datos común empleada para la comunicación entre cliente y servidor. Es necesario que se encuentre en la misma carpeta que cada uno de los programas para su funcionamiento.
- Esta solución sincroniza los tres hilos de ejecución del método ```handle``` en el lado del servidor. En cada iteración, se espera a que se haya recibido mensaje de ayuda de los tres clientes, o bien, se espera a un tiempo de *timeout* antes de enviar el siguiente mensaje.
- Se asume que tanto los clientes como el servidor tienen los relojes bien sincronizados, pues las estampas de tiempo se utilizan para determinar si un mensaje ha expirado.
