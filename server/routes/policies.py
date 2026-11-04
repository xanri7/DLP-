"""Policy administration and agent synchronization API."""
from flask import Blueprint, jsonify, request
from server.policy.manager import PolicyManager

bp = Blueprint("policies", __name__, url_prefix="/api/v1/policies")
manager = PolicyManager()

@bp.get("")
def get_policies():
    return jsonify(manager.get_document())

@bp.get("/version")
def get_policy_version():
    return jsonify({"policy_version": manager.get_document()["policy_version"]})

@bp.post("")
def create_policy():
    payload = request.get_json(silent=True) or {}
    try:
        return jsonify(manager.create(payload)), 201
    except (ValueError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400

@bp.put("/<policy_id>")
def update_policy(policy_id):
    payload = request.get_json(silent=True) or {}
    try:
        return jsonify(manager.update(policy_id, payload))
    except KeyError:
        return jsonify({"error": "Policy not found"}), 404
    except (ValueError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400

@bp.delete("/<policy_id>")
def disable_policy(policy_id):
    try:
        manager.disable(policy_id)
        return jsonify({"status": "disabled", "policy_id": policy_id})
    except KeyError:
        return jsonify({"error": "Policy not found"}), 404
