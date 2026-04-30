from flask import Flask, request, jsonify
import mysql.connector
import os
import requests
from decimal import Decimal, InvalidOperation

app = Flask(__name__)

# =========================
# CONEXIÓN A BASE DE DATOS
# =========================
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# =========================
# CREAR PEDIDO (FLUJO COMPLETO)
# =========================
@app.route("/pedidos", methods=["POST"])
def crear_pedido():
    data = request.json

    # 1. VALIDAR USUARIO
    usuario = requests.get(f"http://auth:5000/usuarios/{data['usuario_id']}").json()

    if "error" in usuario:
        return {"error": "Usuario no encontrado"}, 404

    if usuario["rol"] != "cliente":
        return {"error": "Solo clientes pueden hacer pedidos"}, 403

    total = Decimal("0.00")

    # 2. VALIDAR STOCK
    for item in data["productos"]:
        res = requests.get(
            f"http://inventario:5000/validar-stock/{item['producto_id']}/{item['cantidad']}"
        ).json()

        if not res.get("valido"):
            return {"error": f"Stock insuficiente en producto {item['producto_id']}"}, 400

    conn = get_connection()
    cursor = conn.cursor()

    # 3. CREAR PEDIDO
    cursor.execute(
        "INSERT INTO pedidos (usuario_id, estado, tipo, direccion, total) VALUES (%s,%s,%s,%s,%s)",
        (
            data["usuario_id"],
            "pendiente",
            data["tipo"],
            data.get("direccion"),
            0
        )
    )

    pedido_id = cursor.lastrowid

    # 4. GUARDAR DETALLE Y CALCULAR TOTAL
    productos = requests.get("http://inventario:5000/productos").json()

    try:
        for item in data["productos"]:
            producto_id = int(item["producto_id"])
            cantidad = int(item["cantidad"])

            producto = next((p for p in productos if int(p[0]) == producto_id), None)

            if not producto:
                conn.close()
                return {"error": f"Producto {producto_id} no encontrado"}, 404

            try:
                precio = Decimal(str(producto[3]))
            except (InvalidOperation, TypeError):
                conn.close()
                return {"error": f"Precio inválido para producto {producto_id}"}, 500

            subtotal = precio * Decimal(cantidad)
            total += subtotal

            cursor.execute(
                "INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad) VALUES (%s,%s,%s)",
                (pedido_id, producto_id, cantidad)
            )

            # 5. DESCONTAR STOCK
            requests.post(
                "http://inventario:5000/descontar-stock",
                json={
                    "producto_id": producto_id,
                    "cantidad": cantidad
                }
            )
    except Exception:
        conn.rollback()
        conn.close()
        raise

    # 6. ACTUALIZAR TOTAL
    cursor.execute(
        "UPDATE pedidos SET total=%s WHERE id=%s",
        (str(total), pedido_id)
    )

    conn.commit()
    conn.close()

    return {
        "mensaje": "Pedido creado correctamente",
        "pedido_id": pedido_id,
        "total": float(total)
    }

# =========================
# OBTENER TODOS LOS PEDIDOS
# =========================
@app.route("/pedidos", methods=["GET"])
def obtener_pedidos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.id, p.estado, p.tipo, p.total, u.nombre, p.observacion
        FROM pedidos p
        JOIN usuarios u ON p.usuario_id = u.id
    """)

    pedidos = cursor.fetchall()
    conn.close()

    return jsonify(pedidos)

# =========================
# PEDIDOS POR USUARIO
# =========================
@app.route("/pedidos/usuario/<int:id>", methods=["GET"])
def pedidos_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, estado, tipo, total, observacion
        FROM pedidos
        WHERE usuario_id = %s
    """, (id,))

    pedidos = cursor.fetchall()
    conn.close()

    return jsonify(pedidos)

# =========================
# ACTUALIZAR ESTADO (ADMIN)
# =========================
@app.route("/pedidos/<int:id>/estado", methods=["PUT"])
def actualizar_estado(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT estado FROM pedidos WHERE id=%s", (id,))
    result = cursor.fetchone()

    if not result:
        return {"error": "Pedido no encontrado"}, 404

    estado_actual = result[0]

    if estado_actual == "entregado":
        return {"error": "No se puede modificar un pedido entregado"}, 400

    cursor.execute(
        "UPDATE pedidos SET estado=%s WHERE id=%s",
        (data["estado"], id)
    )

    conn.commit()
    conn.close()

    return {"mensaje": "Estado actualizado"}

# =========================
# RECHAZAR PEDIDO
# =========================
@app.route("/pedidos/<int:id>/rechazar", methods=["PUT"])
def rechazar_pedido(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE pedidos SET estado='rechazado', observacion=%s WHERE id=%s",
        (data["observacion"], id)
    )

    conn.commit()
    conn.close()

    return {"mensaje": "Pedido rechazado"}

# =========================
# DETALLE DE PEDIDO
# =========================
@app.route("/pedidos/<int:id>/detalle", methods=["GET"])
def detalle_pedido(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM pedidos WHERE id=%s",
        (id,)
    )
    if not cursor.fetchone():
        conn.close()
        return {"error": "Pedido no encontrado"}, 404

    cursor.execute("""
        SELECT pr.nombre, dp.cantidad, pr.precio, (dp.cantidad * pr.precio) AS subtotal
        FROM detalle_pedido dp
        JOIN productos pr ON pr.id = dp.producto_id
        WHERE dp.pedido_id = %s
    """, (id,))

    detalle = cursor.fetchall()
    conn.close()

    return jsonify(detalle)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)