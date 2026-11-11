
from contextlib import closing
from database import get_connection


def get_policy_bundle(policy_id):
    if not isinstance(policy_id, str) or not policy_id.strip():
        raise ValueError("Invalid policy ID")

    with closing(get_connection()) as conn:
        policy = conn.execute("""
            SELECT policy_id, name, mode, version
            FROM policies
            WHERE policy_id = ? AND enabled = 1
        """, (policy_id,)).fetchone()

        if policy is None:
            return None

        rules = conn.execute("""
            SELECT rule_id, event_type, channel,
                   source_pattern, destination_type,
                   file_extension, action, priority
            FROM rules
            WHERE policy_id = ? AND enabled = 1
            ORDER BY priority ASC, rule_id ASC
        """, (policy_id,)).fetchall()

    result = dict(policy)
    result["rules"] = [dict(rule) for rule in rules]

    return result
