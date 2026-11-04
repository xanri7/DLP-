"""Agent event ingestion and dashboard event-query API."""
from flask import Blueprint, jsonify, request
from common.schemas import validate_event
from server.database.events import EventRepository

bp = Blueprint("events", __name__, url_prefix="/api/v1/events")
repository = EventRepository()

@bp.get("")
def list_events():
    try:
        limit = min(max(int(request.args.get("limit", 100)), 1), 500)
    except ValueError:
        limit = 100
    events = repository.list_recent(limit)
    return jsonify({"events": events})

@bp.post("")
def ingest_event():
    event = request.get_json(silent=True)
    try:
        validate_event(event)
        repository.add(event)
        return jsonify({"status": "accepted", "event_id": event["event_id"]}), 202
    except (ValueError, TypeError, KeyError) as exc:
        return jsonify({"error": str(exc)}), 400
