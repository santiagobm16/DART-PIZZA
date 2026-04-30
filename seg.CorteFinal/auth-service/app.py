from flask import Flask, request, jsonify, render_template, redirect, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "clave_secreta"  # cambia esto si quieres más seguridad

# =========================
# CONEXIÓN A DB
# =========================
def _db_connect():
    """
    Patrón tipo imagen:
    - 3 intentos
    - timeout corto
    - logs con print
    - códigos HTTP correctos cuando la BD no responde
    """
    for i in range(3):
        try:
            print("[AUTH] Conectando a base de datos...", flush=True)
            return mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                connection_timeout=2,
            ), None
        except mysql.connector.Error as e:
            print(f"[DB ERROR] intento {i+1}: {str(e)}", flush=True)
    return None, ({"error": "Base de datos no disponible"}, 503)


def get_connection():
    conn, err = _db_connect()
    if err:
        raise RuntimeError(err[0].get("error", "DB error"))
    return conn


def _require_session():
    if not session.get("usuario_id"):
        print("[AUTH] No autorizado (sin sesión)", flush=True)
        return {"error": "No autorizado"}, 401
    return None


def _require_json():
    data = request.get_json(silent=True)
    if data is None:
        print("[AUTH] JSON inválido o ausente", flush=True)
        return None, ({"error": "Solicitud incorrecta (JSON requerido)"}, 400)
    return data, None

# =========================
# VISTAS GENERALES
# =========================

@app.route("/")
def inicio():
    return render_template("auth/login.html")

@app.route("/registro", methods=["GET"])
def registro_page():
    return render_template("auth/registro.html")

# =========================
# VISTAS ADMIN
# =========================

@app.route("/admin", methods=["GET"] )
def admin_dashboard():
    if session.get("rol") != "admin":
        return redirect("/")
    return render_template("admin/dashboard.html")

@app.route("/inventario", methods=["GET"])
def inventario():
    if session.get("rol") != "admin":
        return redirect("/")
    return render_template("admin/inventario.html")

# =========================
# VISTAS CLIENTE
# =========================

@app.route("/cliente", methods=["GET"])
def cliente():
    if session.get("rol") != "cliente":
        return redirect("/")
    return render_template("cliente/productos.html")

@app.route("/mis-pedidos", methods=["GET"])
def pedidos_cliente():
    if session.get("rol") != "cliente":
        return redirect("/")
    return render_template("cliente/pedidos.html")

# =========================
# PERFIL (AMBOS)
# =========================

@app.route("/perfil", methods=["GET"])
def perfil():
    if not session.get("usuario_id"):
        return redirect("/")
    conn, err = _db_connect()
    if err:
        payload, code = err
        return jsonify(payload), code

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, email, rol FROM usuarios WHERE id=%s",
            (session["usuario_id"],)
        )
        user = cursor.fetchone()
    except mysql.connector.Error as e:
        print(f"[DB ERROR] perfil: {str(e)}", flush=True)
        return {"error": "Error interno del servidor"}, 500
    finally:
        try:
            conn.close()
        except Exception:
            pass

    if not user:
        session.clear()
        return redirect("/")

    template = "admin/perfil.html" if session.get("rol") == "admin" else "cliente/perfil.html"
    return render_template(
        template,
        user={
            "id": user[0],
            "nombre": user[1],
            "email": user[2],
            "rol": user[3]
        }
    )

# =========================
# REGISTRO
# =========================

@app.route("/registro", methods=["POST"])
def registro():
    print("[AUTH] POST /registro", flush=True)
    data, json_err = _require_json()
    if json_err:
        payload, code = json_err
        return payload, code

    for k in ("nombre", "email", "password", "rol1"):
        if not data.get(k):
            print(f"[AUTH] Registro inválido: falta {k}", flush=True)
            return {"error": f"Solicitud incorrecta (falta {k})"}, 400

    conn, err = _db_connect()
    if err:
        payload, code = err
        return payload, code

    try:
        cursor = conn.cursor()

        # validar correo único
        cursor.execute("SELECT id FROM usuarios WHERE email=%s", (data["email"],))
        if cursor.fetchone():
            return {"error": "Correo ya registrado"}, 400

        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)",
            (data["nombre"], data["email"], data["password"], data["rol1"])
        )

        conn.commit()
    except mysql.connector.Error as e:
        print(f"[DB ERROR] registro: {str(e)}", flush=True)
        return {"error": "Error interno del servidor"}, 500
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return {"mensaje": "Usuario registrado"}, 201

# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():
    print("[AUTH] POST /login", flush=True)
    data, json_err = _require_json()
    if json_err:
        payload, code = json_err
        return payload, code

    if not data.get("email") or not data.get("password"):
        return {"error": "Solicitud incorrecta (email y password requeridos)"}, 400

    conn, err = _db_connect()
    if err:
        payload, code = err
        return payload, code

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, rol FROM usuarios WHERE email=%s AND password=%s",
            (data["email"], data["password"])
        )
        user = cursor.fetchone()
    except mysql.connector.Error as e:
        print(f"[DB ERROR] login: {str(e)}", flush=True)
        return {"error": "Error interno del servidor"}, 500
    finally:
        try:
            conn.close()
        except Exception:
            pass

    if not user:
        return {"error": "Credenciales incorrectas"}, 401

    # guardar sesión
    session["usuario_id"] = user[0]
    session["nombre"] = user[1]
    session["rol"] = user[2]

    return {
        "usuario_id": user[0],
        "nombre": user[1],
        "rol": user[2]
    }

# =========================
# LOGOUT
# =========================

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")

# =========================
# CONSULTAR USUARIO (PARA OTROS MICROSERVICIOS)
# =========================

@app.route("/usuarios/<int:id>", methods=["GET"])
def obtener_usuario(id):
    print(f"[AUTH] GET /usuarios/{id}", flush=True)
    conn, err = _db_connect()
    if err:
        payload, code = err
        return jsonify(payload), code

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, rol FROM usuarios WHERE id=%s",
            (id,)
        )
        user = cursor.fetchone()
    except mysql.connector.Error as e:
        print(f"[DB ERROR] obtener_usuario: {str(e)}", flush=True)
        return {"error": "Error interno del servidor"}, 500
    finally:
        try:
            conn.close()
        except Exception:
            pass

    if not user:
        return {"error": "Usuario no encontrado"}, 404

    return jsonify({
        "id": user[0],
        "nombre": user[1],
        "rol": user[2]
    })

# =========================
# ACTUALIZAR PERFIL
# =========================

@app.route("/perfil", methods=["PUT"])
def actualizar_perfil():
    print("[AUTH] PUT /perfil", flush=True)
    sess_err = _require_session()
    if sess_err:
        payload, code = sess_err["error"], 401
        return {"error": payload}, code

    data, json_err = _require_json()
    if json_err:
        payload, code = json_err
        return payload, code

    if not data.get("nombre") or not data.get("email"):
        return {"error": "Solicitud incorrecta (nombre y email requeridos)"}, 400

    conn, err = _db_connect()
    if err:
        payload, code = err
        return payload, code

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM usuarios WHERE email=%s AND id<>%s",
            (data["email"], session["usuario_id"])
        )
        if cursor.fetchone():
            return {"error": "Correo ya registrado"}, 400

        cursor.execute(
            "UPDATE usuarios SET nombre=%s, email=%s WHERE id=%s",
            (data["nombre"], data["email"], session["usuario_id"])
        )

        conn.commit()
    except mysql.connector.Error as e:
        print(f"[DB ERROR] actualizar_perfil: {str(e)}", flush=True)
        return {"error": "Error interno del servidor"}, 500
    finally:
        try:
            conn.close()
        except Exception:
            pass

    session["nombre"] = data["nombre"]

    return {"mensaje": "Perfil actualizado"}

# =========================
# CAMBIAR CONTRASEÑA
# =========================

@app.route("/cambiar-password", methods=["PUT"])
def cambiar_password():
    print("[AUTH] PUT /cambiar-password", flush=True)
    sess_err = _require_session()
    if sess_err:
        payload, code = sess_err["error"], 401
        return {"error": payload}, code

    data, json_err = _require_json()
    if json_err:
        payload, code = json_err
        return payload, code

    if not data.get("password"):
        return {"error": "Solicitud incorrecta (password requerido)"}, 400

    conn, err = _db_connect()
    if err:
        payload, code = err
        return payload, code

    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET password=%s WHERE id=%s",
            (data["password"], session["usuario_id"])
        )
        conn.commit()
    except mysql.connector.Error as e:
        print(f"[DB ERROR] cambiar_password: {str(e)}", flush=True)
        return {"error": "Error interno del servidor"}, 500
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return {"mensaje": "Contraseña actualizada"}

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)