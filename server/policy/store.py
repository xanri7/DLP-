"""JSON-backed authoritative policy store."""
import json
import os
from pathlib import Path

DEFAULT_DOCUMENT = {"policy_version": 1, "policies": []}

class PolicyStore:
    def __init__(self, path=None):
        self.path = Path(path or os.getenv("DLP_POLICY_PATH", "server/data/policies.json"))

    def load(self):
        if not self.path.exists():
            return dict(DEFAULT_DOCUMENT)
        with self.path.open("r", encoding="utf-8") as stream:
            return json.load(stream)

    def save(self, policy_document):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        with temporary.open("w", encoding="utf-8") as stream:
            json.dump(policy_document, stream, indent=2)
            stream.write("\n")
        temporary.replace(self.path)
