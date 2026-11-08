"""Shared data contracts used by the DLP Agent and Server.

ChannelEvent carries captured content locally inside the Agent.
EventReport contains metadata only and is safe to serialize for reporting.
"""

from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class EventReport:
    """Metadata that can be sent to the Server without raw content."""

    event_id: str
    channel: str
    event_type: str
    timestamp: str
    content_type: str
    content_length: int

    def to_dict(self):
        """Return the report metadata as a plain dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class ChannelEvent:
    """A locally captured activity event passed through the Agent."""

    event_id: str
    channel: str
    event_type: str
    timestamp: str
    content_type: str
    content_length: int
    content: str = field(repr=False)

    def to_report(self):
        """Create a metadata-only report; never include the captured content."""
        return EventReport(
            event_id=self.event_id,
            channel=self.channel,
            event_type=self.event_type,
            timestamp=self.timestamp,
            content_type=self.content_type,
            content_length=self.content_length,
        )
