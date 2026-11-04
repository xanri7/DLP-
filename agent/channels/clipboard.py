"""Windows clipboard channel adapter placeholder."""
from .base import ChannelAdapter

class ClipboardAdapter(ChannelAdapter):
    channel_name = "clipboard"

    def start(self, on_activity):
        raise NotImplementedError("Windows clipboard monitoring is a future implementation step")

    def stop(self):
        pass
