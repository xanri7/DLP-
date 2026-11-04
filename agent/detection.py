"""Basic sensitive-data checks. Raw content stays on the endpoint."""

import re

PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "national_id": re.compile(r"\b\d{9,12}\b"),
    "payment_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}


def scan_text(value):
    findings = []
    for finding_type, pattern in PATTERNS.items():
        count = len(pattern.findall(value or ""))
        if count:
            findings.append({
                "type": finding_type,
                "severity": "high" if finding_type != "email" else "medium",
                "count": count,
            })
    return findings
