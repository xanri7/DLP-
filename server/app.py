"""Central policy server and simple event dashboard."""

import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request

POLICY_FILE = Path(__file__).with_name("policies.json")
EVENTS = []


def read_policies():
    return json.loads(POLICY_FILE.read_text(encoding="utf-8"))


def write_policies(document):
    temporary = POLICY_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(document, indent=2), encoding="utf-8")
    temporary.replace(POLICY_FILE)


def create_app():
    app = Flask(__name__)

    @app.get("/")
    def dashboard():
        return render_template("index.html")

    @app.get("/api/v1/policies")
    def get_policies():
        return jsonify(read_policies())

    @app.put("/api/v1/policies")
    def update_policies():
        document = request.get_json(silent=True)
        if not isinstance(document, dict) or not isinstance(document.get("policies"), list):
            return jsonify(error="Expected a JSON object containing a policies array"), 400
        current = read_policies()
        document["policy_version"] = current.get("policy_version", 0) + 1
        write_policies(document)
        return jsonify(document)

    @app.post("/api/v1/events")
    def receive_event():
        event = request.get_json(silent=True)
        if not isinstance(event, dict):
            return jsonify(error="Expected a JSON event"), 400
        event["event_id"] = len(EVENTS) + 1
        EVENTS.append(event)
        return jsonify(status="received", event_id=event["event_id"]), 201

    @app.get("/api/v1/events")
    def get_events():
        return jsonify(list(reversed(EVENTS)))

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
