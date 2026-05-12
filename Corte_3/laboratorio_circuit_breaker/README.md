## Fase 1 – OBSERVAR (sin modificar código)
•	Apagar el servicio de mascotas
![Apagarservicio](evidencias\Fase1_1.png)

•	Hacer varias peticiones al gateway
![Hacerpeticion](evidencias\Fase1_2.png)
 
•	Revisar logs
![Revisarlogs](evidencias\Fase1_3.png)
 
## Responder:
## ¿Qué hace el sistema actualmente?
Rta: el sistema funciona mediante un gateway que actúa como intermediario entre el cliente y los microservicios.
Cuando el usuario hace una petición a /mascotas, el gateway intenta comunicarse con el servicio backend correspondiente.
Entonces: 
-	Si el servicio está activo: el gateway recibe la respuesta, valida que existan datos y devuelve la información correctamente al cliente.
-	Si el servicio de mascotas se apaga: el gateway detecta que no puede conectarse, captura el error, evita que el sistema completo falle y responde con un mensaje controlado indicando que el servicio no está disponible.
Además, los logs permiten observar: intentos de conexión, errores de comunicación, timeouts y el estado de cada microservicio.

## ¿Se protege o insiste?
Rta: El sistema hace ambas cosas, pero de manera básica.
Se protege, porque: captura excepciones (ConnectionError, Timeout), evita que la aplicación colapse y responde con errores HTTP controlados como 503 Service Unavailable.
Esto demuestra un manejo básico de tolerancia a fallos.

Insiste parcialmente porque:  el gateway tiene un ciclo de hasta 3 intentos.
Sin embargo: los reintentos reales solo ocurren cuando hay Timeout, porque en caso de ConnectionError el sistema retorna inmediatamente y corta el ciclo. 
Por lo tanto:
-	ante lentitud - sí insiste
-	ante caída total del servicio - no insiste realmente.

## Explicación breve (qué hice y qué observe)

En esta fase primeramente apage el servicio de mascotas para simular la caída de un microservicio y posteriormente realize varias peticiones al gateway y los revise atreves de los logs del sistema.

Puede observar que el gateway intentaba comunicarse con el backend y al estar apagado y no encontrarlo disponible, capturaba el error y respondía con mensajes controlados, sin detener completamente el sistema. También se evidenció que existían intentos de conexión y manejo básico de excepciones, aunque todavía no se implementaba un Circuit Breaker completo.
