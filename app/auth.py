from functools import wraps
from flask import request, jsonify, current_app


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return jsonify(
                {
                    "error": "API Key requerida",
                    "message": "Debe proporcionar una API Key en el header X-API-Key",
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
