"""Server-side policy CRUD and version management interface."""
class PolicyManager:
    """Owns policy creation, editing, disablement, and version increments."""
    def list_active(self) -> dict:
        raise NotImplementedError

    def create(self, policy: dict) -> dict:
        raise NotImplementedError

    def update(self, policy_id: str, changes: dict) -> dict:
        raise NotImplementedError

    def disable(self, policy_id: str) -> None:
        raise NotImplementedError
