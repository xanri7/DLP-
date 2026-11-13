"""Local sensitive-data detection for Agent channel events.

Only finding metadata is returned. Raw content remains local to the Agent.
"""

import re


_PATTERNS = {
    "EMAIL_ADDRESS": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),
    "PHONE_NUMBER": re.compile(
        r"(?<!\w)(?:\+?\d[\d\s().-]{5,}\d)(?!\w)"
    ),
    "CREDIT_CARD": re.compile(
        r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)"
    ),
}


def _passes_luhn(value):
    """Return whether a digit sequence passes the Luhn checksum."""
    digits = [int(char) for char in value if char.isdigit()]
    if not 13 <= len(digits) <= 19:
        return False

    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit

    return checksum % 10 == 0


def analyze_event(event):
    """Analyze a ChannelEvent and return metadata about detected patterns."""
    content = event.content
    findings = []

    if _PATTERNS["EMAIL_ADDRESS"].search(content):
        findings.append("EMAIL_ADDRESS")

    valid_card_spans = []
    for match in _PATTERNS["CREDIT_CARD"].finditer(content):
        if _passes_luhn(match.group()):
            valid_card_spans.append(match.span())

    if valid_card_spans:
        findings.append("CREDIT_CARD")

    phone_found = False
    for match in _PATTERNS["PHONE_NUMBER"].finditer(content):
        overlaps_credit_card = any(
            match.start() < card_end and match.end() > card_start
            for card_start, card_end in valid_card_spans
        )
        if not overlaps_credit_card:
            phone_found = True
            break

    if phone_found:
        findings.append("PHONE_NUMBER")

    return {
        "event_id": event.event_id,
        "channel": event.channel,
        "sensitive_types": findings,
        "matched_pattern_ids": [f"{finding}_V1" for finding in findings],
        "detection_count": len(findings),
    }
