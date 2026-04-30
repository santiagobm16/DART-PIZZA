from flask import Flask, request, jsonify
import mysql.connector
import os

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
# CREAR PRODUCTO
# =========================
@app.route("/productos", methods=["POST"])
def crear_producto():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    # Validar nombre único
    cursor.execute("SELECT id FROM productos WHERE nombre=%s", (data["nombre"],))
    existe = cursor.fetchone()

    if existe:
        return {"error": "El producto ya existe"}, 400

    cursor.execute("""
        INSERT INTO productos (nombre, tipo, precio, stock, imagen, activo)
        VALUES (%s, %s, %s, %s, %s, TRUE)
    """, (
        data["nombre"],
        data["tipo"],
        data["precio"],
        data.get("stock"),
        data.get("imagen")
    ))

    conn.commit()
    conn.close()

    return {"mensaje": "Producto creado correctamente"}

# =========================
# OBTENER PRODUCTOS ACTIVOS
# =========================
@app.route("/productos", methods=["GET"])
def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE activo=TRUE")
    productos = cursor.fetchall()

    conn.close()

    return jsonify(productos)

# =========================
# ACTUALIZAR PRODUCTO
# =========================
@app.route("/productos/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE productos
        SET nombre=%s, tipo=%s, precio=%s, stock=%s, imagen=%s
        WHERE id=%s
    """, (
        data["nombre"],
        data["tipo"],
        data["precio"],
        data.get("stock"),
        data.get("imagen"),
        id
    ))

    conn.commit()
    conn.close()

    return {"mensaje": "Producto actualizado"}

# =========================
# ACTIVAR / DESACTIVAR PRODUCTO
# =========================
@app.route("/productos/<int:id>/estado", methods=["PUT"])
def cambiar_estado(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE productos SET activo=%s WHERE id=%s",
        (data["activo"], id)
    )

    conn.commit()
    conn.close()

    return {"mensaje": "Estado actualizado"}

# =========================
# VALIDAR STOCK
# =========================
@app.route("/validar-stock/<int:producto_id>/<int:cantidad>", methods=["GET"])
def validar_stock(producto_id, cantidad):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT stock FROM productos WHERE id=%s AND activo=TRUE",
        (producto_id,)
    )

    result = cursor.fetchone()
    conn.close()

    if not result:
        return {"error": "Producto no disponible"}, 404

    stock = result[0]

    # Productos sin control de stock (pizzas/adiciones)
    if stock is None:
        return {"valido": True}

    if stock >= cantidad:
        return {"valido": True}
    else:
        return {"valido": False, "mensaje": "Stock insuficiente"}

# =========================
# DESCONTAR STOCK
# =========================
@app.route("/descontar-stock", methods=["POST"])
def descontar_stock():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT stock FROM productos WHERE id=%s", (data["producto_id"],))
    result = cursor.fetchone()

    if not result:
        return {"error": "Producto no encontrado"}, 404

    stock = result[0]

    if stock is not None:
        if stock < data["cantidad"]:
            return {"error": "Stock insuficiente"}, 400

        cursor.execute(
            "UPDATE productos SET stock = stock - %s WHERE id=%s",
            (data["cantidad"], data["producto_id"])
        )

    conn.commit()
    conn.close()

    return {"mensaje": "Stock actualizado"}

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)