"""Canonical shared vocabulary and payload builders for Agent and Server."""
CHANNELS = {"clipboard", "usb"}
DECISIONS = {"ALLOW", "WARN", "BLOCK"}
SEVERITIES = {"low", "medium", "high", "critical"}
ENFORCEMENT_STATUSES = {"SUCCESS", "FAILED", "NOT_REQUIRED"}
POLICY_STATUSES = {"enabled", "disabled"}

def make_detection_result(findings):
    return {"sensitive": bool(findings), "findings": findings}

def make_policy_result(decision, reason, policy_id=None):
    decision = decision.upper()
    if decision not in DECISIONS:
        raise ValueError(f"Unsupported decision: {decision}")
    return {"decision": decision, "reason": reason, "policy_id": policy_id}

def validate_policy_document(document):
    if not isinstance(document, dict) or not isinstance(document.get("policy_version"), int):
        raise ValueError("Policy document requires integer policy_version")
    policies = document.get("policies")
    if not isinstance(policies, list):
        raise ValueError("Policy document requires a policies array")
    seen = set()
    for policy in policies:
        required = {"id", "name", "enabled", "channel", "conditions", "action"}
        if not isinstance(policy, dict) or not required.issubset(policy):
            raise ValueError("Policy is missing required fields")
        if policy["id"] in seen:
            raise ValueError("Duplicate policy id")
        seen.add(policy["id"])
        if policy["channel"] not in CHANNELS or policy["action"] not in DECISIONS:
            raise ValueError("Unsupported channel or action")
        if not isinstance(policy["enabled"], bool) or not isinstance(policy["conditions"], dict):
            raise ValueError("Invalid enabled or conditions value")
    return document

def validate_event(event):
    required = {"event_id", "agent_id", "channel", "timestamp", "event_type",
                "findings", "decision", "policy_id", "enforcement_status"}
    if not isinstance(event, dict) or not required.issubset(event):
        raise ValueError("Event is missing required fields")
    if event["channel"] not in CHANNELS or event["decision"] not in DECISIONS:
        raise ValueError("Unsupported event channel or decision")
    if event["enforcement_status"] not in ENFORCEMENT_STATUSES:
        raise ValueError("Unsupported enforcement status")
    if not isinstance(event["findings"], list):
        raise ValueError("findings must be an array")
    return event
