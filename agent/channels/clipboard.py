"""Clipboard monitoring channel.

Polls the system clipboard and emits ChannelEvent objects when text changes.
Raw clipboard content stays inside the Agent for local detection.
"""

import logging
import time
import uuid
from datetime import datetime, timezone

import pyperclip

from common.contracts import ChannelEvent

logger = logging.getLogger(__name__)


def read_clipboard():
    """Return the current clipboard text."""
    return pyperclip.paste()


def create_clipboard_event(content):
    """Wrap captured clipboard text in the Agent's shared event contract."""
    return ChannelEvent(
        event_id=str(uuid.uuid4()),
        channel="CLIPBOARD",
        event_type="COPY",
        timestamp=datetime.now(timezone.utc).isoformat(),
        content_type="TEXT",
        content_length=len(content),
        content=content,
    )


def monitor_clipboard(poll_interval=2.5):
    """Yield a ChannelEvent whenever the clipboard text changes."""
    previous_clipboard = ""

    while True:
        time.sleep(poll_interval)
        current_clipboard = read_clipboard()

        if current_clipboard != previous_clipboard:
            if current_clipboard:
                yield create_clipboard_event(current_clipboard)

            previous_clipboard = current_clipboard


def main():
    """Run the clipboard channel and log metadata for emitted events."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    for event in monitor_clipboard():
        logger.info(
            "Clipboard event detected: event_id=%s content_length=%d",
            event.event_id,
            event.content_length,
        )


if __name__ == "__main__":
    main()
