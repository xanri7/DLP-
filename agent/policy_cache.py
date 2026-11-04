"""Local JSON policy cache used by the endpoint agent."""

import json
from pathlib import Path

CACHE_PATH = Path(__file__).with_name("policy_cache.json")


def load():
    """Load the last cached policy document, if one exists."""
    if not CACHE_PATH.exists():
        return None
    with CACHE_PATH.open("r", encoding="utf-8") as cache_file:
        return json.load(cache_file)


def save(policy_document):
    """Save a policy document received from the server."""
    temporary_path = CACHE_PATH.with_suffix(".tmp")
    with temporary_path.open("w", encoding="utf-8") as cache_file:
        json.dump(policy_document, cache_file, indent=2)
    temporary_path.replace(CACHE_PATH)
