from flask import Blueprint, jsonify
from app.services.eltoque import ElToqueClient
from app.config import Config

api_bp = Blueprint("api", __name__, url_prefix="/v1")


def get_eltoque_client():
    return ElToqueClient()


@api_bp.route("/trmi", methods=["GET"])
def get_trmi():
    client = get_eltoque_client()
    try:
        data = client.get_trmi()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
