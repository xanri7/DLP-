"""Clipboard monitoring channel.

Reads clipboard text and creates structured events for the Agent.
Raw clipboard content stays local for detection.
"""

import logging
import time
import uuid
from datetime import datetime, timezone

import pyperclip

from common.contracts import ChannelEvent

logger = logging.getLogger(__name__)


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


def main():
    prev_clip = ""
    while True:
        time.sleep(2.5)
        current_clip = read_clipboard()
        if current_clip != prev_clip:
            if current_clip:
                event = create_clipboard_event(current_clip)
                logger.info(
                    "Clipboard event detected: event_id=%s content_length=%d",
                    event.event_id,
                    event.content_length,
                )
            prev_clip = current_clip


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    main()
