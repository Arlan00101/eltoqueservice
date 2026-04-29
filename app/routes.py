from flask import Blueprint, jsonify, request, g
from datetime import datetime, timedelta
from app.auth import require_api_key
from app.services.eltoque import ElToqueClient
from app.config import Config

api_bp = Blueprint("api", __name__, url_prefix="/v1")


def get_eltoque_client():
    return ElToqueClient(api_key=Config.ELTOQUE_API_KEY)


@api_bp.route("/salud", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "API funcionando correctamente"}), 200


@api_bp.route("/tasas", methods=["GET"])
@require_api_key
def get_tasas():
    client = get_eltoque_client()
    try:
        data = client.get_all_tasas()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/tasas/informal", methods=["GET"])
@require_api_key
def get_tasas_informales():
    client = get_eltoque_client()
    try:
        data = client.get_tasas_informales()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/tasas/oficial", methods=["GET"])
@require_api_key
def get_tasas_oficiales():
    client = get_eltoque_client()
    try:
        data = client.get_tasas_oficiales()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/tasas/historico", methods=["GET"])
@api_bp.route("/trmi", methods=["GET"])
@require_api_key
def get_tasas_historico():
    date_from = request.args.get("date_from") or request.args.get("fecha_inicio")
    date_to = request.args.get("date_to") or request.args.get("fecha_fin")

    if not date_from or not date_to:
        return jsonify(
            {
                "success": False,
                "error": "Se requieren los parámetros date_from y date_to",
            }
        ), 400

    try:
        dt_from = datetime.strptime(date_from, "%Y-%m-%d %H:%M:%S")
        dt_to = datetime.strptime(date_to, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify(
            {
                "success": False,
                "error": "Formato de fecha inválido. Use YYYY-MM-DD HH:MM:SS",
            }
        ), 400

    diferencia = dt_to - dt_from
    if diferencia > timedelta(hours=24):
        return jsonify(
            {
                "success": False,
                "error": "El rango de fechas no puede exceder las 24 horas",
            }
        ), 400

    client = get_eltoque_client()
    try:
        data = client.get_tasas_historico(date_from, date_to)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
