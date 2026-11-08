"""TODO: Clipboard monitoring channel.

Define the channel interface and event metadata expected by the Agent.
No clipboard monitoring is implemented yet.
"""
import time
import pyperclip

def read_clipboard():
 clip = pyperclip.paste()
 return clip


def main():
 prev_clip = ""
 while True:
   time.sleep(2.5)
   current_clip = (read_clipboard())
   if (current_clip != prev_clip):
    print(current_clip)
    prev_clip = current_clip


if __name__ == '__main__':
    main()
