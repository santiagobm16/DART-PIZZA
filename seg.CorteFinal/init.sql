CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

-- USUARIOS
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    rol ENUM('admin', 'cliente')
);

-- PRODUCTOS
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE,
    tipo ENUM('pizza', 'adicion', 'bebida'),
    precio DECIMAL(10,2),
    stock INT DEFAULT NULL,
    imagen VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE
);

-- PEDIDOS
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    estado ENUM('pendiente','preparando','enviado','entregado','rechazado'),
    tipo ENUM('local','domicilio'),
    direccion VARCHAR(255),
    total DECIMAL(10,2),
    observacion TEXT
);

-- DETALLE PEDIDO
CREATE TABLE detalle_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    producto_id INT,
    cantidad INT
);

-- =========================
-- DATOS DE PRUEBA (10 REGISTROS)
-- =========================

-- USUARIOS (2)
INSERT INTO usuarios (nombre, email, password, rol) VALUES
('Admin Principal', 'admin@pizza.com', '1234', 'admin'),
('Juan Cliente', 'cliente@pizza.com', '1234', 'cliente');

-- PRODUCTOS (8)
INSERT INTO productos (nombre, tipo, precio, stock,imagen, activo) VALUES
('Pizza Hawaiana', 'pizza', 25000, NULL, "https://pizzarte.pe/cdn/shop/files/IMG_3651_1024x.jpg?v=1738892066",TRUE),
('Pizza Pepperoni', 'pizza', 28000, NULL, "https://www.hunts.com/sites/g/files/qyyrlu211/files/uploadedImages/img_6934_48664.jpg",TRUE),
('Pizza Vegetariana', 'pizza', 30000, NULL, "https://www.unileverfoodsolutions.es/dam/global-ufs/mcos/SPAIN/calcmenu/recipes/ES-recipes/general/pizza-barbacoa/main-header.jpg", TRUE),

('Queso Extra', 'adicion', 3000, NULL, "https://colanta.com/aprende-de/wp-content/uploads/2019/01/Queso-mozzarella-1.jpg", TRUE),
('Tocineta', 'adicion', 4000, NULL, "https://enriko.com.co/storage/2021/05/TOCINETA-ESTANDAR-1.jpg", TRUE),

('Coca Cola 400ml', 'bebida', 5000, 20, "https://www.coca-cola.com/content/dam/onexp/co/es/brands/coca-cola/coca-cola-original/ccso_600ml_750x750.png", TRUE),
('Sprite 400ml', 'bebida', 4500, 15, "https://product-images.farmatodo.com/hXU6chNfa9HugiIPaG2GI3Yj-CWX6laKStdgL1sZ_4pD8kaI-GkHGjjzXd4fVX7Dfjdcg6EuEOgfua-ba3jYIGlia5C2mp3N6-3H6EahQcItfKSE", TRUE),
('Agua 600ml', 'bebida', 3000, 30, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlBQACV_9SJz5DQ3x7NBiPmDyhGWDRytVISw&s", TRUE);

-- 🔹 PEDIDOS (relacionados con usuarios)
INSERT INTO pedidos (usuario_id, estado, tipo, direccion, total, observacion) VALUES
(2, 'pendiente', 'domicilio', 'Calle 10 #5-20', 33000, NULL),
(2, 'preparando', 'local', NULL, 28000, NULL),
(2, 'enviado', 'domicilio', 'Carrera 8 #12-30', 35000, NULL),
(2, 'entregado', 'local', NULL, 25000, NULL),
(2, 'rechazado', 'domicilio', 'Calle 15 #9-40', 30000, 'Producto sin disponibilidad');

-- 🔹 DETALLE PEDIDO (relacionado con pedidos y productos)
INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad) VALUES

-- Pedido 1
(1, 1, 1),  -- Pizza Hawaiana
(1, 6, 1),  -- Coca Cola

-- Pedido 2
(2, 2, 1),  -- Pizza Pepperoni

-- Pedido 3
(3, 3, 1),  -- Pizza BBQ
(3, 7, 1),  -- Pepsi

-- Pedido 4
(4, 1, 1),  -- Pizza Hawaiana

-- Pedido 5
(5, 2, 1);  -- Pizza Pepperoni