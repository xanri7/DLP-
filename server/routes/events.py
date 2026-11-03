"""Agent event ingestion and event-query endpoints."""
from flask import Blueprint, jsonify

bp = Blueprint("events", __name__, url_prefix="/api/v1/events")

@bp.route("", methods=["GET", "POST"])
def events():
    return jsonify({"error": "Event API is not implemented yet"}), 501
