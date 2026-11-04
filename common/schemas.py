"""Canonical shared vocabulary and payload builders for Agent and Server."""
CHANNELS = {"clipboard", "usb"}
DECISIONS = {"ALLOW", "WARN", "BLOCK"}
SEVERITIES = {"low", "medium", "high", "critical"}
ENFORCEMENT_STATUSES = {"SUCCESS", "FAILED", "NOT_REQUIRED"}
POLICY_STATUSES = {"enabled", "disabled"}
EVENT_TYPES = {"clipboard_change", "file_copy", "file_access"}

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
    ids = set()
    for policy in policies:
        if not isinstance(policy, dict):
            raise ValueError("Each policy must be an object")
        required = {"id", "name", "enabled", "channel", "conditions", "action"}
        if not required.issubset(policy):
            raise ValueError(f"Policy is missing fields: {sorted(required - set(policy))}")
        if policy["id"] in ids:
            raise ValueError(f"Duplicate policy id: {policy['id']}")
        ids.add(policy["id"])
        if policy["channel"] not in CHANNELS:
            raise ValueError(f"Unsupported channel: {policy['channel']}")
        if policy["action"] not in DECISIONS:
            raise ValueError(f"Unsupported action: {policy['action']}")
        if not isinstance(policy["enabled"], bool) or not isinstance(policy["conditions"], dict):
            raise ValueError("enabled must be boolean and conditions must be an object")
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
