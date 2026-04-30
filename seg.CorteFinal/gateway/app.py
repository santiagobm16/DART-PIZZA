from flask import Flask, request, jsonify, Response, abort
from flask_cors import CORS
import requests

# Desactivamos el static handler por defecto de Flask en gateway
# para que la ruta `/static/...` sea proxyeada al auth-service.
app = Flask(__name__, static_folder=None)
CORS(app, resources={r"/api/*": {"origins": "*"}})

AUTH_URL = "http://auth:5000"
INVENTARIO_URL = "http://inventario:5000"
PEDIDOS_URL = "http://pedidos:5000"

_HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-encoding",
    "content-length",
}


def _proxy_auth(path: str):
    upstream_url = f"{AUTH_URL}{path}"

    headers = {
        k: v
        for k, v in request.headers.items()
        if k.lower() not in {"host"} and not k.lower().startswith("sec-")
    }

    upstream = requests.request(
        method=request.method,
        url=upstream_url,
        params=request.args,
        data=request.get_data(),
        headers=headers,
        cookies=request.cookies,
        allow_redirects=False,
        timeout=15,
    )

    response_headers = []
    for k, v in upstream.headers.items():
        lk = k.lower()
        if lk in _HOP_BY_HOP_HEADERS:
            continue

        if lk == "location" and isinstance(v, str):
            v = v.replace(AUTH_URL, "")

        response_headers.append((k, v))

    return Response(upstream.content, status=upstream.status_code, headers=response_headers)


def _forward_json(method: str, url: str):
    resp = requests.request(method=method, url=url, json=request.json, timeout=15)
    return jsonify(resp.json()), resp.status_code


@app.route("/health", methods=["GET"])
def health():
    return {"mensaje": "Gateway funcionando correctamente"}


# Proxy “catch-all” de vistas del auth-service desde el puerto 5000
@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
def auth_pages_proxy(path: str):
    if path.startswith("api/") or path == "health":
        abort(404)

    upstream_path = f"/{path}" if path else "/"
    return _proxy_auth(upstream_path)


# =========================
# API (CONSUMIDO POR FRONT)
# =========================

@app.route("/api/productos", methods=["GET", "POST"])
def api_productos():
    if request.method == "GET":
        resp = requests.get(f"{INVENTARIO_URL}/productos", timeout=15)
        return jsonify(resp.json()), resp.status_code
    return _forward_json("POST", f"{INVENTARIO_URL}/productos")


@app.route("/api/productos/<int:id>", methods=["PUT"])
def api_actualizar_producto(id: int):
    return _forward_json("PUT", f"{INVENTARIO_URL}/productos/{id}")


@app.route("/api/productos/<int:id>/estado", methods=["PUT"])
def api_estado_producto(id: int):
    return _forward_json("PUT", f"{INVENTARIO_URL}/productos/{id}/estado")


@app.route("/api/pedidos", methods=["GET", "POST"])
def api_pedidos():
    if request.method == "GET":
        resp = requests.get(f"{PEDIDOS_URL}/pedidos", timeout=15)
        return jsonify(resp.json()), resp.status_code
    return _forward_json("POST", f"{PEDIDOS_URL}/pedidos")


@app.route("/api/pedidos/<int:id>/estado", methods=["PUT"])
def api_estado_pedido(id: int):
    return _forward_json("PUT", f"{PEDIDOS_URL}/pedidos/{id}/estado")


@app.route("/api/pedidos/<int:id>/rechazar", methods=["PUT"])
def api_rechazar_pedido(id: int):
    return _forward_json("PUT", f"{PEDIDOS_URL}/pedidos/{id}/rechazar")


@app.route("/api/pedidos/usuario/<int:id>", methods=["GET"])
def api_pedidos_usuario(id: int):
    resp = requests.get(f"{PEDIDOS_URL}/pedidos/usuario/{id}", timeout=15)
    return jsonify(resp.json()), resp.status_code


@app.route("/api/pedidos/<int:id>/detalle", methods=["GET"])
def api_detalle_pedido(id: int):
    resp = requests.get(f"{PEDIDOS_URL}/pedidos/{id}/detalle", timeout=15)
    return jsonify(resp.json()), resp.status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)