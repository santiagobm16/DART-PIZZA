# DART-PIZZA
# PARTE 1 — ENTENDER EL PROBLEMA
1. ¿Qué problema resuelve el sistema?
Rta:la falta de una plataforma digital eficiente para la pizzeria que apenas este iniciando, que le permita llevar el stock de esta y llevar un control de los gastos y las ventas. Permitira a los clientes realizar pedidos y pagos de forma rapida y visual.
2. ¿Quién lo usará?
Rta: En Nuestro caso los roles seria el de Administrador y Cliente.
- Administrador: podra gestionar productos, inventario, pedidos, gastos y ventas.
- Cliente: podra registrarse,visualizar los productos, realizar los pedidos y pagos.
3. ¿Qué pasaría si no existiera?
Rta: Sin el sistema, la pizzería tendria una gestión manual e ineficiente, lo que limita sus ventas ya que estamos en un entorno donde las aplicaciones digitales dominan el mercado.

# PARTE 2 – IDENTIFICAR LOS SERVICIOS
1. ¿Qué funciones principales tiene el sistema?
Rta: 
- Registro y autenticación
- Gestión de inventario y productos
- Gestión de pedidos
- Pago
- Historial de gastos y ventas
- Notificaciones
2. ¿Qué partes pueden trabajar por separado? 
Rta:
- Registro y autenticación
- Inventario y productos
- Pedidos
- Pagos
- Notificaciones
- Historial de gastos y ventas
3. ¿Qué procesos son independientes?
Rta:
- Inventario: atuliazar stock y productos
- Pagos: confirmación de transacciones
- Notificaciones: envío de avisos al cliente y administrador

# PARTE 3 – ¿CÓMO SE COMUNICAN?
1. ¿Qué servicio necesita información de otro?
Rta:
- Pedidos → solicita → inventario
- Pedidos → registra → historial de ventas

- Cliente → solicita → autenticación
- Cliente → solicita → productos

- Administrador → solicita → inventario
- administrador → solicita → historial de gastos  
2. ¿Quién solicita datos?
Rta:
- Pedidos → solicita → inventario
- Pedidos → solicita → pagos

- Cliente → solicita → autenticación
- Cliente → solicita → productos

- Administrador → solicita → inventario
- Administrador → solicita → historial de gastos
3. ¿Quién responde?
Rta:
- Inventario → responde → pedidos
- historial de ventas → responde → pedidos

- Autenticación → valida → cliente
- Productos → responde → cliente

- Inventario → responde → administrador
- Historial de gastos → responde → administrador

# PARTE 4 – ELEGIR LA ARQUITECTURA
Decidan cuál usarán:
Rta:elegimos
- Microservicios
Preguntas guía:
1. ¿Cuántos usuarios tendrá el sistema?
Rta: por un inicio el sistema tendra pocos usuarios entre 50 y 100. A medida que la pizzeria sea mas conocida tendra mas usuarios.
2. ¿Necesita escalar?
Rta: si, porque se espera tener muchos mas usuarios y poder integrarle algunas funciones al sistema. 
3. ¿Es un sistema pequeño o grande?
Rta: por el momento es un sistema pequeño que hace lo esencial.
Justifiquen su elección:
Elegimos esta arquitectura porque tiene tolerancia a fallos, debido a que permite dividir el sistema en servicios independientes, ya que si un servicio falla, los demas pueden seguir funcionando sin afectar todo el sistema, ademas cada servicio puede desarrollarse y mejorarse de manera independiente.

# PARTE 5 – BASE DE DATOS
1. ¿Qué información debe guardarse?
Rta:
- Usuarios
- Productos
- Inventario
- Pedidos
- Pagos
- Historial de gastos y ventas 
2. ¿Qué datos son críticos?
Rta:
- Pedidos
- Pagos
- Inventario
- Información de usuarios
3. ¿Qué pasaría si se pierden?
Rta: esto afectaria gravemente el funcionamiento del negocio, porque generaria errores en los pedidos y esto genera perdidas económicas y una inestabilidad en el historial de gastos y ventas.

# PARTE 6 – FALLAS Y RIESGOS
1. ¿Quién usará el sistema?
Rta:
- Administrador
- Cliente
2. Pregunta clave:
¿Todos pueden hacer lo mismo?
Rta: no, el administrador gestiona los productos, el inventario, los pedidos y ve el historial financiero. Mientras que el cliente solo se registra, inicia sesión, ve los productos, realiza pedidos y pagos.
4. Pregunta clave:
¿Todos los servicios usan la misma base de datos o cada uno tiene la suya?
Rta: no, cada servicio es independiente y maneja su propia base de datos.

# PARTE 7 — FALLAS Y RIESGOS
Pensar como ingenieros reales
¿Qué pasaría si falla:
- servicio de pagos: podrian suceder dos situaciones, la primera es que el cliente no pueda finalizar su pedido y la segunda es que si finalice el pedido pero el pago no se efectue generando perdidas a la pizzería.
- base de datos: en el caso de que esta falle no habra información sobre los usuarios, impidiendo su inicio de sesión. También no mostraria los productos impidiendo realizar los pedidos y pagos.
- servidor principal: si este llega a fallar el administrador y los usuarios no podran acceder a la plataforma.
Escriban posibles soluciones:
- reintentos: automatizar el pago para que si no se efectua vuelva a intentarlo hasta que se genere y notificar al usuario sobre el estado de la transaccion y al administrador si se hizo el pago correctamente. 
- notificaciones:
- respaldo de datos: generar una copia de seguridad semanalmente en la base de datos, lo que ayudaría a conservar la información, pero la información que se ingrese despues de la copia no quedara registrada y por ello se perdera.
