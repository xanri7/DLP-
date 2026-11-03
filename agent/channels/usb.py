"""USB extraction channel; Windows implementation is pending."""
from .base import BaseChannel

class USBChannel(BaseChannel):
    name = "usb"

    def start(self) -> None:
        raise NotImplementedError("Implement Windows removable-drive monitoring.")

    def stop(self) -> None:
        raise NotImplementedError

    def handle_activity(self, activity: dict) -> None:
        raise NotImplementedError
