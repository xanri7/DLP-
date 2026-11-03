"""Agent registration and heartbeat endpoints."""
from flask import Blueprint, jsonify

bp = Blueprint("agents", __name__, url_prefix="/api/v1/agents")

@bp.post("/heartbeat")
def heartbeat():
    return jsonify({"error": "Heartbeat is not implemented yet"}), 501
