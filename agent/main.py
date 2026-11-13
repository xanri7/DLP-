"""Agent entry point.

Starts the clipboard channel and sends captured events through local detection.
"""

import logging

from agent.channels.clipboard import monitor_clipboard
from agent.detection import analyze_event


def configure_logging():
    frmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format=frmt,
    )


def main():
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("DLP Agent has started")

    for event in monitor_clipboard():
        result = analyze_event(event)

        if result["detection_count"] > 0:
            logger.warning(
                "Sensitive data detected: event_id=%s channel=%s "
                "types=%s detection_count=%d",
                result["event_id"],
                result["channel"],
                result["sensitive_types"],
                result["detection_count"],
            )
        else:
            logger.info(
                "Clipboard event analyzed: event_id=%s no sensitive patterns found",
                result["event_id"],
            )


if __name__ == '__main__':
    main()
