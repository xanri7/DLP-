"""Clipboard monitoring channel; Windows implementation is pending."""
from .base import BaseChannel

class ClipboardChannel(BaseChannel):
    name = "clipboard"

    def start(self) -> None:
        raise NotImplementedError("Implement Windows clipboard monitoring.")

    def stop(self) -> None:
        raise NotImplementedError

    def handle_activity(self, activity: dict) -> None:
        raise NotImplementedError
