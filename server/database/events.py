"""Persistence interface for security events."""
class EventRepository:
    def add(self, event: dict) -> None:
        raise NotImplementedError

    def list_recent(self, limit: int = 100) -> list[dict]:
        raise NotImplementedError
