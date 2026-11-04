"""Prototype enforcement actions."""


def enforce(decision, channel):
    # Clipboard blocking is performed by clearing the clipboard in the
    # clipboard channel. USB blocking needs a later OS-level implementation.
    if decision == "BLOCK" and channel == "clipboard":
        return "PENDING_CHANNEL_ACTION"
    if decision == "BLOCK" and channel == "usb":
        return "NOT_SUPPORTED"
    return "NOT_REQUIRED"
