"""USB extraction channel adapter placeholder."""
from .base import ChannelAdapter

class USBAdapter(ChannelAdapter):
    channel_name = "usb"

    def start(self, on_activity):
        raise NotImplementedError("Windows USB monitoring is a future implementation step")

    def stop(self):
        pass
