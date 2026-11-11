
import sqlite3
from uuid import uuid4
import json
from pathlib import Path
from contextlib import closing


# 1. Database Configuration
DB_PATH = Path(__file__).resolve().parent / "neon_sentinel.db"


# 2. Database Connection
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# 3. Initialize Database
def init_db():
    with closing(get_connection()) as conn:
        with conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    channel TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    findings_metadata TEXT NOT NULL DEFAULT '{}',
                    decision TEXT,
                    policy_id TEXT,
                    enforcement_status TEXT NOT NULL DEFAULT 'UNKNOWN',
                    received_at TEXT NOT NULL DEFAULT
                        (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
                );

                CREATE INDEX IF NOT EXISTS idx_events_agent_time
                ON events(agent_id, timestamp);
                
CREATE TABLE IF NOT EXISTS policies (
    policy_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    enabled INTEGER NOT NULL DEFAULT 1
        CHECK (enabled IN (0, 1)),
    mode TEXT NOT NULL DEFAULT 'MONITOR'
        CHECK (mode IN ('MONITOR', 'ENFORCE')),
    version INTEGER NOT NULL DEFAULT 1
        CHECK (version >= 1),
    created_at TEXT NOT NULL DEFAULT
        (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT
        (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
                    
                CREATE TABLE IF NOT EXISTS rules (
                    rule_id TEXT PRIMARY KEY,
                    policy_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    channel TEXT NOT NULL,
                    source_pattern TEXT,
                    destination_type TEXT,
                    file_extension TEXT,
                    action TEXT NOT NULL
                        CHECK (action IN ('ALLOW', 'BLOCK', 'ALERT')),
                    priority INTEGER NOT NULL DEFAULT 100,
                    enabled INTEGER NOT NULL DEFAULT 1
                        CHECK (enabled IN (0, 1)),
                    FOREIGN KEY (policy_id)
                        REFERENCES policies(policy_id)
                        ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_rules_policy
                ON rules(policy_id);
""")


# 4. Save Agent Events
def save_event(event):
    required = (
        "event_id", "agent_id", "channel",
        "event_type", "timestamp"
    )

    # Validate required fields
    for field in required:
        if not isinstance(event.get(field), str) or not event[field].strip():
            raise ValueError(f"Invalid or missing field: {field}")

    # Validate metadata
    metadata = event.get("findings_metadata", {})

    allowed_metadata = {
        "file_extension", "file_size",
        "source_type", "destination_type"
    }

    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary")

    if set(metadata) - allowed_metadata:
        raise ValueError("Unsupported metadata fields")

    # Insert event into SQLite
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute("""
                INSERT INTO events (
                    event_id, agent_id, channel,
                    event_type, timestamp, findings_metadata,
                    decision, policy_id, enforcement_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(event_id) DO NOTHING
            """, (
                event["event_id"],
                event["agent_id"],
                event["channel"],
                event["event_type"],
                event["timestamp"],
                json.dumps(metadata),
                event.get("decision"),
                event.get("policy_id"),
                event.get("enforcement_status", "UNKNOWN")
            ))

            return cursor.rowcount == 1
        
# 5. Retrieve stored events
def get_events(limit=50):
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100")

    with closing(get_connection()) as conn:
        rows = conn.execute("""
            SELECT * FROM events
            ORDER BY received_at DESC, event_id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    events = [dict(row) for row in rows]

    for event in events:
        event["findings_metadata"] = json.loads(
            event["findings_metadata"]
        )

    return events


# 6. Create a new security policy
def create_policy(name, description="", mode="MONITOR"):

    if not isinstance(name, str) or not 1 <= len(name.strip()) <= 100:
        raise ValueError("Invalid policy name")

    if not isinstance(description, str) or len(description) > 500:
        raise ValueError("Invalid policy description")

    if mode not in ("MONITOR", "ENFORCE"):
        raise ValueError("Invalid policy mode")

    policy_id = str(uuid4())

    with closing(get_connection()) as conn:
        with conn:
            conn.execute("""
                INSERT INTO policies (
                    policy_id, name, description, mode
                )
                VALUES (?, ?, ?, ?)
            """, (
                policy_id, name.strip(), description, mode
            ))

    return policy_id


# 7. Create a security rule
def create_rule(policy_id, event_type, channel, action,
                source_pattern=None, destination_type=None,
                file_extension=None, priority=100):

    required = {
        "policy_id": policy_id,
        "event_type": event_type,
        "channel": channel,
        "action": action
    }

    for name, value in required.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Invalid field: {name}")

    if action not in ("ALLOW", "BLOCK", "ALERT"):
        raise ValueError("Invalid rule action")

    if type(priority) is not int or not 1 <= priority <= 1000:
        raise ValueError("Invalid priority")

    for value in (source_pattern, destination_type, file_extension):
        if value is not None and not isinstance(value, str):
            raise ValueError("Invalid rule condition")

    rule_id = str(uuid4())

    with closing(get_connection()) as conn:
        with conn:
            policy = conn.execute(
                "SELECT 1 FROM policies WHERE policy_id = ?",
                (policy_id,)
            ).fetchone()

            if policy is None:
                raise ValueError("Policy does not exist")

            conn.execute("""
                INSERT INTO rules (
                    rule_id, policy_id, event_type, channel,
                    source_pattern, destination_type,
                    file_extension, action, priority
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                rule_id, policy_id, event_type, channel,
                source_pattern, destination_type,
                file_extension, action, priority
            ))

            conn.execute("""
                UPDATE policies
                SET version = version + 1,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
                WHERE policy_id = ?
            """, (policy_id,))

    return rule_id



# 5. Application Entry Point
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")
