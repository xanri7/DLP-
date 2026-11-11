
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import closing
import database
import policies
with TemporaryDirectory() as folder:
    database.DB_PATH = Path(folder) / "test.db"
    database.init_db()

    event = {
        "event_id": "test-001",
        "agent_id": "LAB-PC-01",
        "channel": "USB",
        "event_type": "FILE_COPY",
        "timestamp": "2026-11-11T12:00:00Z",
        "findings_metadata": {
            "file_extension": ".pdf",
            "destination_type": "USB"
        },
        "decision": "BLOCK",
        "enforcement_status": "SIMULATED"
    }

    print("First insert:", database.save_event(event))
    print("Duplicate insert:", database.save_event(event))

    with closing(database.get_connection()) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM events"
        ).fetchone()[0]

    print("Total events:", count)

    events = database.get_events()

    print("Retrieved events:", len(events))
    print("Agent ID:", events[0]["agent_id"])
    print("Event Type:", events[0]["event_type"])
    print("Metadata:", events[0]["findings_metadata"])


    # Test policies table
    with closing(database.get_connection()) as conn:
        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(policies)")
        }

        count = conn.execute(
            "SELECT COUNT(*) FROM policies"
        ).fetchone()[0]

    print("Policies table created:", "policy_id" in columns)
    print("Policies count:", count)


    
    policy_id = database.create_policy(
        name="Protect Lab Files",
        description="Monitor sensitive lab files",
        mode="MONITOR"
    )

    with closing(database.get_connection()) as conn:
        policy = conn.execute(
            "SELECT * FROM policies WHERE policy_id = ?",
            (policy_id,)
        ).fetchone()

    print("Policy created:", policy is not None)
    print("Policy name:", policy["name"])
    print("Policy mode:", policy["mode"])
    print("Policy version:", policy["version"])

    # Test Rules table
    with closing(database.get_connection()) as conn:
        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(rules)")
        }

        count = conn.execute(
            "SELECT COUNT(*) FROM rules"
        ).fetchone()[0]

    print("Rules table created:", "rule_id" in columns)
    print("Rules count:", count)

    rule_id = database.create_rule(
        policy_id=policy_id,
        event_type="FILE_COPY",
        channel="USB",
        action="BLOCK",
        destination_type="USB",
        file_extension=".pdf"
    )

    with closing(database.get_connection()) as conn:
        rule = conn.execute(
            "SELECT * FROM rules WHERE rule_id = ?",
            (rule_id,)
        ).fetchone()

        version = conn.execute(
            "SELECT version FROM policies WHERE policy_id = ?",
            (policy_id,)
        ).fetchone()["version"]

    print("Rule created:", rule is not None)
    print("Rule action:", rule["action"])
    print("Rule extension:", rule["file_extension"])
    print("Policy version after rule:", version)

    bundle = policies.get_policy_bundle(policy_id)

    print("Bundle name:", bundle["name"])
    print("Bundle mode:", bundle["mode"])
    print("Bundle version:", bundle["version"])
    print("Bundle rules:", len(bundle["rules"]))
    print("First rule action:", bundle["rules"][0]["action"])
