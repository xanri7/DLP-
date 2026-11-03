"""SQLite-backed local policy cache and offline event queue interface."""
class LocalStore:
    def save_policy_cache(self, version: int, policies: list[dict]) -> None:
        raise NotImplementedError

    def load_policy_cache(self) -> tuple[int, list[dict]]:
        raise NotImplementedError

    def queue_event(self, event: dict) -> None:
        raise NotImplementedError

    def pending_events(self) -> list[dict]:
        raise NotImplementedError
