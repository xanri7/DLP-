"""Common interface implemented by every monitoring channel."""
from abc import ABC, abstractmethod
from typing import Any

class BaseChannel(ABC):
    name: str

    @abstractmethod
    def start(self) -> None:
        """Start channel monitoring."""

    @abstractmethod
    def stop(self) -> None:
        """Stop channel monitoring."""

    @abstractmethod
    def handle_activity(self, activity: dict[str, Any]) -> None:
        """Normalize and forward activity to the shared DLP pipeline."""
