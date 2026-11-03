"""Server-side policy synchronization service interface."""
class SynchronizationService:
    def current_policy_version(self) -> int:
        raise NotImplementedError

    def policies_for_agent(self, known_version: int) -> dict | None:
        raise NotImplementedError
