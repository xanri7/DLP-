"""Load the agent's cached policies and evaluate an event."""

import json
from pathlib import Path

CACHE_FILE = Path(__file__).with_name("policies_cache.json")


def load_cache():
    if not CACHE_FILE.exists():
        return {"policy_version": 0, "policies": []}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"policy_version": 0, "policies": []}


def save_cache(document):
    temporary = CACHE_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(document, indent=2), encoding="utf-8")
    temporary.replace(CACHE_FILE)


def decide(channel, findings, document):
    if not findings:
        return "ALLOW", None
    for policy in document.get("policies", []):
        if not policy.get("enabled", True) or policy.get("channel") not in (channel, "all"):
            continue
        return policy.get("action", "WARN"), policy.get("id")
    return "WARN", None
