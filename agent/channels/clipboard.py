"""Clipboard monitoring channel.

Polls the system clipboard for text changes and creates local channel events.
This is a prototype: it does not yet perform detection or enforce policies.
"""

import time
import uuid
from datetime import datetime, timezone

import pyperclip

from common.contracts import ChannelEvent


POLL_INTERVAL_SECONDS = 2.5


def read_clipboard():
    """Return the current clipboard text without modifying it."""
    return pyperclip.paste()


def create_clipboard_event(content):
    """Wrap captured clipboard text and its metadata in a channel event."""
    return ChannelEvent(
        event_id=str(uuid.uuid4()),
        channel="clipboard",
        event_type="clipboard_change",
        timestamp=datetime.now(timezone.utc).isoformat(),
        content_type="text/plain",
        content_length=len(content),
        content=content,
    )


def monitor_clipboard(poll_interval=POLL_INTERVAL_SECONDS):
    """Poll for clipboard changes and display a local test event."""
    previous_clip = None

    print("Clipboard monitoring started. Press Ctrl+C to stop.")

    try:
        while True:
            current_clip = read_clipboard()

            if current_clip != previous_clip:
                if current_clip:
                    event = create_clipboard_event(current_clip)

                    # Display content for local testing only.
                    print("\nClipboard change detected:")
                    print(event.content)
                    print("Event metadata:", event.to_report().to_dict())

                previous_clip = current_clip

            time.sleep(poll_interval)

    except KeyboardInterrupt:
        print("\nClipboard monitoring stopped.")


def main():
    monitor_clipboard()


if __name__ == "__main__":
    main()
