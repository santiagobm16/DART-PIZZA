from flask import Flask, request, jsonify
import requests
import time

app= Flask(__name__)

circuito_abierto_usuarios = False
fallos_usuarios = 0
segundo_reintento_usuarios = 0
ESPERA_REINTENTO_USUARIOS = 10

circuito_abierto_mascotas = False
fallos_mascotas = 0
segundo_reintento_mascotas = 0
ESPERA_REINTENTO_MASCOTAS = 10

circuito_abierto_resumen = False
fallos_resumen = 0
segundo_reintento_resumen = 0
ESPERA_REINTENTO_RESUMEN = 10

@app.route("/usuarios")
def usuarios():
    global circuito_abierto_usuarios, fallos_usuarios, segundo_reintento_usuarios
    if circuito_abierto_usuarios:
        ahora = time.time()
        if ahora < segundo_reintento_usuarios:
            return jsonify({"error": "Servicios temporalemente bloquedado."}), 503

        print("[GATEWAY] Reintento controlado usuarios (half-open)...", flush=True)
        try:
            response = requests.get("http://usuarios:5000/usuarios", timeout=2)
            if response.status_code == 200:
                data = response.json()
                if data:
                    circuito_abierto_usuarios = False
                    fallos_usuarios = 0
                    print("[GATEWAY] Usuarios recuperado, circuito cerrado.", flush=True)
                    return jsonify(data)

            segundo_reintento_usuarios = time.time() + ESPERA_REINTENTO_USUARIOS
            print("[GATEWAY] Usuarios sigue fallando, circuito reabierto.", flush=True)
            return jsonify({"error": "Se intento conectar de nuevo, pero sigue fallando."}), 503
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            segundo_reintento_usuarios = time.time() + ESPERA_REINTENTO_USUARIOS
            print("[GATEWAY] Usuarios sigue caido, circuito reabierto.", flush=True)
            return jsonify({"error": "Se intento conectar de nuevo, pero sigue fallando."}), 503

    for i in range(3):
        try:
            print("[GATEWAY] llamando a usuarios...", flush=True)
            response = requests.get("http://usuarios:5000/usuarios", timeout=2)
            data = response.json()

            if(response.status_code != 200):
                print("[ERROR] Backend usuarios respondió mal", flush=True)
                return jsonify({"error": "Error en backend usuarios"}), response.status_code

            if not data:
                print("[ERROR] No hay datos que mostrar", flush=True)
                return {"error": "No hay datos"}, 404

            print("[GATEWAY] Usuarios respondió con éxito", flush=True)
            fallos_usuarios = 0
            return jsonify(response.json())

        except requests.exceptions.ConnectionError:
            fallos_usuarios += 1
            print(f"Numero de fallos usuarios: {fallos_usuarios}", flush=True)
            if fallos_usuarios >= 3:
                circuito_abierto_usuarios = True
                segundo_reintento_usuarios = time.time() + ESPERA_REINTENTO_USUARIOS
                print("El circuito breaker usuarios es True.", flush=True)
            print("[ERROR] Servicio usuarios caído", flush=True)
            return {"error": "Servicio no disponible"}, 503

        except requests.exceptions.Timeout:
            fallos_usuarios += 1
            print(f"Numero de fallos usuarios: {fallos_usuarios}", flush=True)
            if fallos_usuarios >= 3:
                circuito_abierto_usuarios = True
                segundo_reintento_usuarios = time.time() + ESPERA_REINTENTO_USUARIOS
                print("El circuito breaker usuarios es True.", flush=True)
                return {"error": "Servicio no disponible."}, 503
            print(f"Timeout intento {i+1}", flush=True)

    return {"error": "Servicio no responde"}, 504

@app.route("/mascotas")
def mascotas():
    global circuito_abierto_mascotas, fallos_mascotas, segundo_reintento_mascotas
    if circuito_abierto_mascotas:
        ahora = time.time()
        if ahora < segundo_reintento_mascotas:
            return jsonify({"error": "Servicios temporalemente bloquedado."}), 503

        print("[GATEWAY] Reintento controlado mascotas (half-open)...", flush=True)
        try:
            response = requests.get("http://backend:5000/mascotas", timeout=2)
            if response.status_code == 200:
                data = response.json()
                circuito_abierto_mascotas = False
                fallos_mascotas = 0
                print("[GATEWAY] Mascotas recuperado, circuito cerrado.", flush=True)
                return jsonify(data)

            segundo_reintento_mascotas = time.time() + ESPERA_REINTENTO_MASCOTAS
            print("[GATEWAY] Mascotas sigue fallando, circuito reabierto.", flush=True)
            return jsonify({"error": "Se intento conectar de nuevo, pero sigue fallando."}), 503
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            segundo_reintento_mascotas = time.time() + ESPERA_REINTENTO_MASCOTAS
            print("[GATEWAY] Mascotas sigue caido, circuito reabierto.", flush=True)
            return jsonify({"error": "Se intento conectar de nuevo, pero sigue fallando."}), 503

    for i in range(3):
        try:
            print("[GATEWAY] llamando a backend...", flush=True)
            response = requests.get("http://backend:5000/mascotas", timeout=2)
            if(response.status_code != 200):
                print("[ERROR] Backend respondió mal", flush=True)
                return jsonify({"error": "Error en backend"}), response.status_code
            data = response.json()
            if not data:
                print("[ERROR] No hay datos que mostrar", flush=True)
                return {"error": "No hay datos"}, 404
            print("[GATEWAY] Backend respondió con éxito", flush=True)
            fallos_mascotas = 0
            return jsonify(response.json())

        except requests.exceptions.ConnectionError:
            fallos_mascotas += 1
            print(f"Numero de fallos mascotas: {fallos_mascotas}", flush=True)
            if fallos_mascotas >= 3:
                circuito_abierto_mascotas = True
                segundo_reintento_mascotas = time.time() + ESPERA_REINTENTO_MASCOTAS
                print("El circuito breaker mascotas es True.", flush=True)
            print("[ERROR] Backend caído", flush=True)
            return {"error": "Servicio no disponible"}, 503

        except requests.exceptions.Timeout:
            fallos_mascotas += 1
            print(f"Numero de fallos mascotas: {fallos_mascotas}", flush=True)
            if fallos_mascotas >= 3:
                circuito_abierto_mascotas = True
                segundo_reintento_mascotas = time.time() + ESPERA_REINTENTO_MASCOTAS
                print("El circuito breaker mascotas es True.", flush=True)
                return {"error": "Servicio no disponible."}, 503
            print(f"Timeout intento {i+1}", flush=True)

    return {"error": "Servicio no responde"}, 504

@app.route("/mascotas/<int:id>")
def mascota_por_id(id):
    global circuito_abierto_mascotas, fallos_mascotas, segundo_reintento_mascotas
    if circuito_abierto_mascotas:
        ahora = time.time()
        if ahora < segundo_reintento_mascotas:
            return jsonify({"error": "Servicios temporalemente bloquedado."}), 503

        print(f"[GATEWAY] Reintento controlado mascota id {id} (half-open)...", flush=True)
        try:
            response = requests.get(f"http://backend:5000/mascotas/{id}", timeout=2)
            if response.status_code == 200:
                data = response.json()
                circuito_abierto_mascotas = False
                fallos_mascotas = 0
                print("[GATEWAY] Mascotas recuperado, circuito cerrado.", flush=True)
                return jsonify(data)

            segundo_reintento_mascotas = time.time() + ESPERA_REINTENTO_MASCOTAS
            print("[GATEWAY] Mascotas sigue fallando, circuito reabierto.", flush=True)
            return jsonify({"error": "Servicio no disponible."}), 503
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            segundo_reintento_mascotas = time.time() + ESPERA_REINTENTO_MASCOTAS
            print("[GATEWAY] Mascotas sigue caido, circuito reabierto.", flush=True)
            return jsonify({"error": "Servicio no disponible."}), 503

    for i in range(3):
        try:
            print(f"[GATEWAY] llamando a backend mascota id {id}...", flush=True)
            response = requests.get(f"http://backend:5000/mascotas/{id}", timeout=2)

            if response.status_code != 200:
                print("[ERROR] Backend respondió mal", flush=True)
                return jsonify({"error": "Error en backend"}), response.status_code

            data = response.json()

            if not data:
                print("[ERROR] No hay datos que mostrar", flush=True)
                return {"error": "No hay datos"}, 404

            print("[GATEWAY] Backend respondió con éxito", flush=True)
            fallos_mascotas = 0
            return jsonify(data)

        except requests.exceptions.ConnectionError:
            fallos_mascotas += 1
            print(f"Numero de fallos mascotas: {fallos_mascotas}", flush=True)
            if fallos_mascotas >= 3:
                circuito_abierto_mascotas = True
                segundo_reintento_mascotas = time.time() + ESPERA_REINTENTO_MASCOTAS
                print("El circuito breaker mascotas es True.", flush=True)
            print("[ERROR] Backend caído", flush=True)
            return {"error": "Servicio no disponible"}, 503

        except requests.exceptions.Timeout:
            fallos_mascotas += 1
            print(f"Numero de fallos mascotas: {fallos_mascotas}", flush=True)
            if fallos_mascotas >= 3:
                circuito_abierto_mascotas = True
                segundo_reintento_mascotas = time.time() + ESPERA_REINTENTO_MASCOTAS
                print("El circuito breaker mascotas es True.", flush=True)
                return {"error": "Servicio no disponible."}, 503
            print(f"Timeout intento {i+1}", flush=True)

    return {"error": "Servicio no responde"}, 504



@app.route("/resumen")
def resumen():
    global circuito_abierto_resumen, fallos_resumen, segundo_reintento_resumen
    if circuito_abierto_resumen:
        ahora = time.time()
        if ahora < segundo_reintento_resumen:
            return jsonify({"error": "Servicios temporalemente bloquedado."}), 503

        print("[GATEWAY] Reintento controlado resumen (half-open)...", flush=True)
        try:
            usuarios_response = requests.get("http://usuarios:5000/usuarios", timeout=2)
            mascotas_response = requests.get("http://backend:5000/mascotas", timeout=2)

            if usuarios_response.status_code == 200 and mascotas_response.status_code == 200:
                usuarios_data = usuarios_response.json()
                mascotas_data = mascotas_response.json()
                if usuarios_data and mascotas_data:
                    circuito_abierto_resumen = False
                    fallos_resumen = 0
                    print("[GATEWAY] Resumen recuperado, circuito cerrado.", flush=True)
                    return jsonify({"usuarios": usuarios_data, "mascotas": mascotas_data})

            segundo_reintento_resumen = time.time() + ESPERA_REINTENTO_RESUMEN
            print("[GATEWAY] Resumen sigue fallando, circuito reabierto.", flush=True)
            return jsonify({"error": "Se intento conectar de nuevo, pero sigue fallando."}), 503
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            segundo_reintento_resumen = time.time() + ESPERA_REINTENTO_RESUMEN
            print("[GATEWAY] Resumen sigue caido, circuito reabierto.", flush=True)
            return jsonify({"error": "Se intento conectar de nuevo, pero sigue fallando."}), 503

    # Fetch usuarios
    usuarios_data = None
    for i in range(3):
        try:
            print("[GATEWAY] llamando a usuarios...", flush=True)
            response = requests.get("http://usuarios:5000/usuarios", timeout=2)
            data = response.json()
            if response.status_code != 200:
                print("[ERROR] Usuarios respondió mal", flush=True)
                continue
            if not data:
                print("[ERROR] No hay datos usuarios", flush=True)
                continue
            usuarios_data = data
            print("[GATEWAY] Usuarios respondió con éxito", flush=True)
            break
        except requests.exceptions.ConnectionError:
            fallos_resumen += 1
            print(f"Numero de fallos resumen: {fallos_resumen}", flush=True)
            if fallos_resumen >= 3:
                circuito_abierto_resumen = True
                segundo_reintento_resumen = time.time() + ESPERA_REINTENTO_RESUMEN
                print("El circuito breaker resumen es True.", flush=True)
                return {"error": "Servicio no disponible."}, 503
            print("[ERROR] Servicio usuarios caído", flush=True)
            continue
        except requests.exceptions.Timeout:
            fallos_resumen += 1
            print(f"Numero de fallos resumen: {fallos_resumen}", flush=True)
            if fallos_resumen >= 3:
                circuito_abierto_resumen = True
                segundo_reintento_resumen = time.time() + ESPERA_REINTENTO_RESUMEN
                print("El circuito breaker resumen es True.", flush=True)
                return {"error": "Servicio no disponible."}, 503
            print(f"Timeout intento {i+1} usuarios", flush=True)
            continue
    if usuarios_data is None:
        fallos_resumen += 1
        print(f"Numero de fallos resumen: {fallos_resumen}", flush=True)
        if fallos_resumen >= 3:
            circuito_abierto_resumen = True
            segundo_reintento_resumen = time.time() + ESPERA_REINTENTO_RESUMEN
            print("El circuito breaker resumen es True.", flush=True)
        return {"error": "Servicio usuarios no responde"}, 504

    # Fetch mascotas
    mascotas_data = None
    for i in range(3):
        try:
            print("[GATEWAY] llamando a backend...", flush=True)
            response = requests.get("http://backend:5000/mascotas", timeout=2)
            data = response.json()
            if response.status_code != 200:
                print("[ERROR] Backend respondió mal", flush=True)
                continue
            if not data:
                print("[ERROR] No hay datos mascotas", flush=True)
                continue
            mascotas_data = data
            print("[GATEWAY] Backend respondió con éxito", flush=True)
            break
        except requests.exceptions.ConnectionError:
            fallos_resumen += 1
            print(f"Numero de fallos resumen: {fallos_resumen}", flush=True)
            if fallos_resumen >= 3:
                circuito_abierto_resumen = True
                segundo_reintento_resumen = time.time() + ESPERA_REINTENTO_RESUMEN
                print("El circuito breaker resumen es True.", flush=True)
                return {"error": "Servicio no disponible."}, 503
            print("[ERROR] Backend caído", flush=True)
            continue
        except requests.exceptions.Timeout:
            fallos_resumen += 1
            print(f"Numero de fallos resumen: {fallos_resumen}", flush=True)
            if fallos_resumen >= 3:
                circuito_abierto_resumen = True
                segundo_reintento_resumen = time.time() + ESPERA_REINTENTO_RESUMEN
                print("El circuito breaker resumen es True.", flush=True)
                return {"error": "Servicio no disponible."}, 503
            print(f"Timeout intento {i+1} mascotas", flush=True)
            continue
    if mascotas_data is None:
        fallos_resumen += 1
        print(f"Numero de fallos resumen: {fallos_resumen}", flush=True)
        if fallos_resumen >= 3:
            circuito_abierto_resumen = True
            segundo_reintento_resumen = time.time() + ESPERA_REINTENTO_RESUMEN
            print("El circuito breaker resumen es True.", flush=True)
        return {"error": "Servicio mascotas no responde"}, 504

    fallos_resumen = 0
    return jsonify({"usuarios": usuarios_data, "mascotas": mascotas_data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)