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

