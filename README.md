# DART-PIZZA

## PARTE 1 — ENTENDER EL PROBLEMA

1. ¿Qué problema resuelve el sistema?  
Rta: la falta de una plataforma digital eficiente para la pizzeria que apenas este iniciando, que le permita llevar el stock de esta y llevar un control de los gastos y las ventas. Permitira a los clientes realizar pedidos y pagos de forma rapida y visual.

2. ¿Quién lo usará?  
Rta: En Nuestro caso los roles seria el de Administrador y Cliente.
- Administrador: podra gestionar productos, inventario, pedidos, gastos y ventas.
- Cliente: podra registrarse, visualizar los productos, realizar los pedidos y pagos.

3. ¿Qué pasaría si no existiera?  

Rta: Sin el sistema, la pizzería tendria una gestión manual e ineficiente, lo que limita sus ventas ya que estamos en un entorno donde las aplicaciones digitales dominan el mercado.

---

## PARTE 2 – IDENTIFICAR LOS SERVICIOS

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
- Inventario: actualizar stock y productos
- Pagos: confirmación de transacciones
- Notificaciones: envío de avisos al cliente y administrador

---

## PARTE 3 – ¿CÓMO SE COMUNICAN?

1. ¿Qué servicio necesita información de otro?  
Rta:
- Pedidos → solicita → inventario
- Pedidos → registra → historial de ventas
- Cliente → solicita → autenticación
- Cliente → solicita → productos
- Administrador → solicita → inventario
- Administrador → solicita → historial de gastos

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
- Historial de ventas → responde → pedidos
- Autenticación → valida → cliente
- Productos → responde → cliente
- Inventario → responde → administrador
- Historial de gastos → responde → administrador

---

## PARTE 4 – ELEGIR LA ARQUITECTURA

Decidan cuál usarán:  
Rta: elegimos
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

---

## PARTE 5 – BASE DE DATOS

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

4. Pregunta clave: ¿Todos los servicios usan la misma base de datos o cada uno tiene la suya?  
Rta: no, cada servicio es independiente y maneja su propia base de datos.

---

## PARTE 6 – ROLES Y PERMISOS

1. ¿Quién usará el sistema?  
Rta:
- Administrador
- Cliente

2. Pregunta clave: ¿Todos pueden hacer lo mismo?  
Rta: no, el administrador gestiona los productos, el inventario, los pedidos y ve el historial financiero. Mientras que el cliente solo se registra, inicia sesión, ve los productos, realiza pedidos y pagos.

---

## PARTE 7 — FALLAS Y RIESGOS

Pensar como ingenieros reales. ¿Qué pasaría si falla:

- **Servicio de pagos:** podrian suceder dos situaciones, la primera es que el cliente no pueda finalizar su pedido y la segunda es que si finalice el pedido pero el pago no se efectue generando perdidas a la pizzería.
- **Base de datos:** en el caso de que esta falle no habra información sobre los usuarios, impidiendo su inicio de sesión. También no mostraria los productos impidiendo realizar los pedidos y pagos.
- **Servidor principal:** si este llega a fallar el administrador y los usuarios no podran acceder a la plataforma.

Posibles soluciones:
- **Reintentos:** automatizar el pago para que si no se efectua vuelva a intentarlo hasta que se genere y notificar al usuario sobre el estado de la transaccion y al administrador si se hizo el pago correctamente.
- **Notificaciones:** avisar en tiempo real al cliente y al administrador sobre el estado de cada operación crítica.
- **Respaldo de datos:** generar una copia de seguridad semanalmente en la base de datos, lo que ayudaría a conservar la información, pero la información que se ingrese despues de la copia no quedara registrada y por ello se perdera.

---

## 📁 Estructura del proyecto
```
dart-pizza/
├── .gitignore
├── Dockerfile
├── README.md
│
├── api-rest/               ← API con Node.js y Express
│   ├── Dockerfile
│   ├── index.js
│   ├── package.json
│   └── package-lock.json
│
├── compose-demo/           ← Demo con Docker Compose (Nginx + MySQL)
│   └── docker-compose.yml
│
├── sitio/                  ← Sitio web estático servido con Nginx
│   └── linktree.html
│
├── actividades/            ← Actividades anteriores del curso
│   └── actividad-anterior.html
│
└── docs/                   ← Documentos del trabajo universitario
    ├── analisis.docx
    └── presentacion.pdf
```

---

## 🚀 Instalación y ejecución

### Requisitos previos

Asegúrate de tener instalado:
- [Docker](https://www.docker.com/get-started) (versión 20 o superior)
- [Docker Compose](https://docs.docker.com/compose/install/) (versión 2 o superior)
- [Git](https://git-scm.com/)

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/dart-pizza.git
cd dart-pizza
```

### 2. Sitio web (Nginx)

Desde la raíz del proyecto (`dart-pizza/`):
```bash
docker build -t dart-pizza-sitio .
docker run -d -p 8080:80 --name sitio dart-pizza-sitio
```

Abre en el navegador: [http://localhost:8080/linktree.html](http://localhost:8080/linktree.html)

### 3. API REST (Node.js + Express)
```bash
cd api-rest
npm install
docker build -t dart-pizza-api .
docker run -d -p 3000:3000 --name apirest dart-pizza-api
```

Endpoints disponibles:

| Endpoint | Descripción |
|---|---|
| [http://localhost:3000/usuarios](http://localhost:3000/usuarios) | Servicio de usuarios |
| [http://localhost:3000/pedidos](http://localhost:3000/pedidos) | Servicio de pedidos |

### 4. Demo con Docker Compose
```bash
cd compose-demo
docker compose up -d
```

Esto levanta:
- **Nginx** en [http://localhost:8082](http://localhost:8082)
- **MySQL** con contraseña root: `1234`

Para detenerlo:
```bash
docker compose down
```

### 5. Detener contenedores individuales
```bash
docker stop sitio apirest
docker rm sitio apirest
```

# DART-PIZZA SEGUNDA ENTREGA
## Descripción del proyecto.
rta: El proyecto consiste en el desarrollo de una aplicación web para la gestión de una pizzería, que permite a los clientes registrarse, iniciar sesión, visualizar productos y realizar pedidos, mientras que el administrador puede gestionar el inventario y dar seguimiento a los pedidos. El sistema está construido bajo una arquitectura de microservicios utilizando Flask, donde se separan las funcionalidades en servicios independientes: autenticación, inventario y pedidos, coordinados a través de un gateway que actúa como punto único de entrada. Estos servicios se comunican entre sí mediante HTTP dentro de un entorno contenerizado con Docker, y utilizan una base de datos MySQL para la persistencia de la información.
## Instrucciones claras para ejecución.
rta: Instrucciones para ejecución
# 1. Crear entorno virtual
En la raíz del proyecto ejecutar:
## python -m venv venv

# 2. Activar entorno virtual
En Windows:
## venv\Scripts\activate

# 3. Instalar dependencias
## pip install -r requirements.txt

# 4. Ejecutar el sistema
Opción (Docker):
## docker-compose up --build

# 5. Acceder al sistema
Abrir en el navegador:
## http://localhost:5000
## Descripción básica de endpoints.
## Gateway (uso principal – frontend)
GET /api/productos - Obtiene la lista de productos activos desde el servicio de inventario.
POST /api/productos - Permite crear un nuevo producto en el inventario.
PUT /api/productos/<id> - Actualiza la información de un producto existente.
PUT /api/productos/<id>/estado - Activa o desactiva un producto.
GET /api/pedidos - Lista todos los pedidos registrados.
POST /api/pedidos - Crea un nuevo pedido (incluye validación de usuario y stock).
PUT /api/pedidos/<id>/estado - Actualiza el estado de un pedido (preparando, enviado, entregado).
PUT /api/pedidos/<id>/rechazar - Permite rechazar un pedido con una observación.
GET /api/pedidos/usuario/<id> - Consulta los pedidos asociados a un usuario específico.
GET /api/pedidos/<id>/detalle - Muestra el detalle de productos de un pedido.
## Auth Service (usuarios)
POST /registro - Registra un nuevo usuario en el sistema.
POST /login - Inicia sesión y crea una sesión de usuario.
GET /logout - Cierra la sesión del usuario.
GET /perfil - Obtiene la información del usuario autenticado.
PUT /perfil - Permite actualizar los datos del usuario.
PUT /cambiar-password - Permite cambiar la contraseña del usuario.
GET /usuarios/<id> - Retorna información básica de un usuario (usado por otros servicios).
## Inventario Service (productos y stock)
GET /productos - Lista todos los productos activos.
POST /productos - Crea un nuevo producto.
PUT /productos/<id> - Actualiza la información de un producto.
PUT /productos/<id>/estado - Activa o desactiva un producto.
GET /validar-stock/<producto_id>/<cantidad> - Verifica si hay suficiente stock disponible.
POST /descontar-stock - Reduce el stock de un producto después de un pedido.
## Pedidos Service (gestión de pedidos)
POST /pedidos - Crea un nuevo pedido validando usuario y stock.
GET /pedidos - Lista todos los pedidos.
GET /pedidos/usuario/<id> - Obtiene los pedidos de un usuario específico.
PUT /pedidos/<id>/estado - Cambia el estado del pedido.
PUT /pedidos/<id>/rechazar - Marca un pedido como rechazado con una observación.
GET /pedidos/<id>/detalle - Muestra el detalle de productos de un pedido.
