"""HTTPS synchronization client interface."""
class SyncClient:
    def check_policy_version(self) -> int:
        raise NotImplementedError

    def download_policies(self, version: int) -> dict:
        raise NotImplementedError

    def upload_events(self, events: list[dict]) -> None:
        raise NotImplementedError

    def send_heartbeat(self) -> None:
        raise NotImplementedError
