from functools import wraps
from flask import request, jsonify, current_app


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        auth_header = request.headers.get("Authorization", "")

        if auth_header.startswith("Bearer "):
            return f(*args, **kwargs)

        if not api_key:
            return jsonify(
                {
                    "error": "API Key requerida",
                    "message": "Debe proporcionar una API Key en el header X-API-Key o Authorization: Bearer <token>",
                }
            ), 401

        expected_key = current_app.config.get("API_KEY")

        if not expected_key:
            return jsonify(
                {
                    "error": "Configuración error",
                    "message": "API no configurada correctamente",
                }
            ), 500

        if api_key != expected_key:
            return jsonify(
                {
                    "error": "API Key inválida",
                    "message": "La API Key proporcionada no es válida",
                }
            ), 403

        return f(*args, **kwargs)

    return decorated_function
