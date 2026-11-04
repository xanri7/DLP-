"""Poll the Windows clipboard and pass changed text to a callback."""

import time

import pyperclip


def monitor(on_text, interval=1.0):
    previous = None
    while True:
        try:
            current = pyperclip.paste()
            if current and current != previous:
                previous = current
                on_text(current)
        except Exception as error:
            print(f"[clipboard] {error}")
        time.sleep(interval)
