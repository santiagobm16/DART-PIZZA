from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

# CONFIGURACIÓN GENERAL

SERVICIOS = {
    "usuarios": {
        "url": "http://usuarios:5000/usuarios",
        "fallos": 0,
        "circuito": False, #estado circuito false=funciona normal, true=bloqueado
        "reintento": 0
    },

    "mascotas": {
        "url": "http://backend:5000/mascotas",
        "fallos": 0,
        "circuito": False,
        "reintento": 0
    }
}
#variables globales
MAX_FALLOS = 5 # fallos antes de generarse el bloqueo
TIEMPO_ESPERA = 5 #espera 5 seg antes de volver a intentar

# FUNCIÓN CIRCUIT BREAKER

def consultar_servicio(nombre_servicio):

    servicio = SERVICIOS[nombre_servicio]


    # CIRCUITO ABIERTO

    if servicio["circuito"]:

        ahora = time.time()

        if ahora < servicio["reintento"]:
            print(f"[CIRCUIT OPEN] {nombre_servicio} bloqueado", flush=True)

            return {
                "error": f"Servicio {nombre_servicio} temporalmente bloqueado"
            }, 503

      
        # HALF OPEN

        print(f"[HALF OPEN] Reintentando conexion con {nombre_servicio}", flush=True)

        try: #intenta llamar al servicio, y solo entra si el servicio responde a 200

            response = requests.get(servicio["url"], timeout=2)

            if response.status_code == 200:

                servicio["circuito"] = False
                servicio["fallos"] = 0

                print(f"[RECUPERADO] {nombre_servicio} volvio a funcionar", flush=True)

                return response.json(), 200

            servicio["reintento"] = time.time() + TIEMPO_ESPERA #se programa nuevo intento

            return {
                "error": f"{nombre_servicio} intento 1, sigue fallando"
            }, 503

        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout):

            servicio["reintento"] = time.time() + TIEMPO_ESPERA #se programa nuevo intento

            print(f"[ERROR] {nombre_servicio} sigue caido", flush=True)

            return {
                "error": f"{nombre_servicio} intento 2, sigue caido"
            }, 503


    # INTENTOS NORMALES

    for intento in range(3): #llama 3 veces al servicio

        try:

            print(f"[REQUEST] Llamando servicio {nombre_servicio}", flush=True)

            response = requests.get(servicio["url"], timeout=2)

            if response.status_code != 200: #si el servicio responde mal 

                print(f"[ERROR] {nombre_servicio} respondio mal", flush=True)

                continue

            data = response.json()

            if not data: #si el servicio no trae datos

                print(f"[ERROR] {nombre_servicio} no tiene datos", flush=True)

                continue

            servicio["fallos"] = 0 

            print(f"[OK] {nombre_servicio} respondio correctamente", flush=True)

            return data, 200

        except requests.exceptions.ConnectionError: 

            servicio["fallos"] += 1 #suma fallos

            print(
                f"[ERROR] conexión fallida {nombre_servicio} | Fallos: {servicio['fallos']}",
                flush=True
            )

        except requests.exceptions.Timeout:

            servicio["fallos"] += 1

            print(
                f"[TIMEOUT] {nombre_servicio} | Fallos: {servicio['fallos']}",
                flush=True
            )

  
    # ABRIR CIRCUITO

    if servicio["fallos"] >= MAX_FALLOS:

        servicio["circuito"] = True #bloquea llamadas futuras
        servicio["reintento"] = time.time() + TIEMPO_ESPERA

        print(f"[CIRCUIT OPEN] {nombre_servicio} abierto", flush=True)

    return {
        "error": f"Servicio {nombre_servicio} no disponible"
    }, 503



# RUTA USUARIOS 

@app.route("/usuarios")
def usuarios():

    data, status = consultar_servicio("usuarios")

    return jsonify(data), status


# RUTA MASCOTAS

@app.route("/mascotas")
def mascotas():

    data, status = consultar_servicio("mascotas")

    return jsonify(data), status


# RESUMEN

@app.route("/resumen")
def resumen():

    usuarios_data, usuarios_status = consultar_servicio("usuarios")

    if usuarios_status != 200:
        return jsonify({
            "error": "usuarios no disponible"
        }), usuarios_status

    mascotas_data, mascotas_status = consultar_servicio("mascotas")

    if mascotas_status != 200:
        return jsonify({
            "error": "mascotas no disponible"
        }), mascotas_status

    return jsonify({
        "usuarios": usuarios_data,
        "mascotas": mascotas_data
    })


# MAIN

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
