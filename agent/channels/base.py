"""Interface for pluggable monitoring channels."""
from abc import ABC, abstractmethod

class ChannelAdapter(ABC):
    channel_name: str

    @abstractmethod
    def start(self, on_activity):
        """Start monitoring and pass normalized activity metadata to callback."""
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError
