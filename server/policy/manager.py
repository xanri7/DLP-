"""Server-side policy CRUD and version management."""
from uuid import uuid4
from common.schemas import validate_policy_document
from .store import PolicyStore

class PolicyManager:
    def __init__(self, store=None):
        self.store = store or PolicyStore()

    def get_document(self):
        return self.store.load()

    def create(self, policy):
        document = self.store.load()
        policy = dict(policy)
        policy.setdefault("id", "POL-" + uuid4().hex[:8].upper())
        document["policies"].append(policy)
        document["policy_version"] += 1
        validate_policy_document(document)
        self.store.save(document)
        return policy

    def update(self, policy_id, changes):
        document = self.store.load()
        for index, policy in enumerate(document["policies"]):
            if policy["id"] == policy_id:
                document["policies"][index] = dict(policy, **changes)
                document["policies"][index]["id"] = policy_id
                document["policy_version"] += 1
                validate_policy_document(document)
                self.store.save(document)
                return document["policies"][index]
        raise KeyError(policy_id)

    def disable(self, policy_id):
        return self.update(policy_id, {"enabled": False})
