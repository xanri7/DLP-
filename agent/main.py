"""Endpoint agent entry point.

Run with: python -m agent.main
Set DLP_SERVER_URL to the server address before starting.
"""

import os
import threading
import uuid
from datetime import datetime, timezone

from agent.channels import clipboard, usb
from agent.client import ServerClient
from agent.detection import scan_text
from agent.policy import decide, load_cache, save_cache
from agent.enforcement import enforce

AGENT_ID = os.getenv("DLP_AGENT_ID", str(uuid.uuid4()))
SERVER_URL = os.getenv("DLP_SERVER_URL", "http://127.0.0.1:5000")


def main():
    client = ServerClient(SERVER_URL)
    policies = load_cache()

    try:
        policies = client.get_policies()
        save_cache(policies)
        print("Downloaded policies from server.")
    except Exception as error:
        print(f"Server unavailable; using cached policies: {error}")

    def report(channel, event_type, text_value=""):
        findings = scan_text(text_value)
        decision, policy_id = decide(channel, findings, policies)
        status = enforce(decision, channel)

        # Never send clipboard text or file contents to the server.
        event = {
            "agent_id": AGENT_ID,
            "channel": channel,
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "findings": findings,
            "decision": decision,
            "policy_id": policy_id,
            "enforcement_status": status,
        }
        print(f"{channel}: {event_type} -> {decision}")
        try:
            client.send_event(event)
        except Exception as error:
            print(f"Could not report event: {error}")

    def clipboard_callback(value):
        report("clipboard", "clipboard_changed", value)

    def usb_callback(action, device, mountpoint):
        report("usb", f"usb_{action}")

    threading.Thread(target=clipboard.monitor, args=(clipboard_callback,), daemon=True).start()
    threading.Thread(target=usb.monitor, args=(usb_callback,), daemon=True).start()
    print(f"Agent running. Server: {SERVER_URL}")
    threading.Event().wait()


if __name__ == "__main__":
    main()
