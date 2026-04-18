from flask import Blueprint, jsonify, request
from app.auth import require_api_key
from app.services.eltoque import ElToqueClient

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/salud", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "API funcionando correctamente"}), 200


@api_bp.route("/tasas", methods=["GET"])
@require_api_key
def get_tasas():
    client = ElToqueClient()
    try:
        data = client.get_all_tasas()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/tasas/informal", methods=["GET"])
@require_api_key
def get_tasas_informales():
    client = ElToqueClient()
    try:
        data = client.get_tasas_informales()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/tasas/oficial", methods=["GET"])
@require_api_key
def get_tasas_oficiales():
    client = ElToqueClient()
    try:
        data = client.get_tasas_oficiales()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/tasas/historico", methods=["GET"])
@require_api_key
def get_tasas_historico():
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    tipo = request.args.get("tipo", "informal")

    if not fecha_inicio or not fecha_fin:
        return jsonify(
            {
                "success": False,
                "error": "Se requieren los parámetros fecha_inicio y fecha_fin",
            }
        ), 400

    client = ElToqueClient()
    try:
        data = client.get_tasas_historico(fecha_inicio, fecha_fin, tipo)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
