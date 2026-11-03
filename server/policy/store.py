"""Authoritative central policy persistence interface."""
class PolicyStore:
    def load(self) -> dict:
        raise NotImplementedError

    def save(self, policy_document: dict) -> None:
        raise NotImplementedError
