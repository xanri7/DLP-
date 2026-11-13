"""Clipboard monitoring channel.

Reads clipboard text and creates structured events for the Agent.
Raw clipboard content stays local for detection.
"""

import time
import uuid
from datetime import datetime, timezone

import pyperclip

from common.contracts import ChannelEvent


def read_clipboard():
    clip = pyperclip.paste()
    return clip


def create_clipboard_event(content):
    """Create a structured event from newly detected clipboard text."""
    event = ChannelEvent(
        event_id=str(uuid.uuid4()),
        channel="CLIPBOARD",
        event_type="COPY",
        timestamp=datetime.now(timezone.utc).isoformat(),
        content_type="TEXT",
        content_length=len(content),
        content=content,
    )
    return event


def monitor_clipboard():
    """Yield an event whenever clipboard text changes."""
    prev_clip = ""
    while True:
        time.sleep(2.5)
        current_clip = read_clipboard()
        if current_clip != prev_clip:
            if current_clip:
                event = create_clipboard_event(current_clip)
                yield event
            prev_clip = current_clip


def main():
    """Allow this channel to be run independently for basic testing."""
    for event in monitor_clipboard():
        print(f"Clipboard event created: {event.event_id}")


if __name__ == '__main__':
    main()
