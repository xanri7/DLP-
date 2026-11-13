VERSION=1
DDL=[
"""CREATE TABLE administrators(
admin_id TEXT PRIMARY KEY, username TEXT NOT NULL COLLATE NOCASE UNIQUE,
password_hash TEXT NOT NULL, password_salt TEXT NOT NULL,
is_active INTEGER NOT NULL DEFAULT 1 CHECK(is_active IN(0,1)),
created_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')), last_login_at TEXT)""",
"""CREATE TABLE devices(
device_id TEXT PRIMARY KEY, hostname TEXT NOT NULL, platform TEXT NOT NULL,
status TEXT NOT NULL DEFAULT 'PENDING' CHECK(status IN('PENDING','ONLINE','OFFLINE','DISABLED')),
registered_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')),
last_seen_at TEXT, notes TEXT NOT NULL DEFAULT '')""",
"""CREATE TABLE policies(
policy_id TEXT PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL DEFAULT '',
enabled INTEGER NOT NULL DEFAULT 1 CHECK(enabled IN(0,1)),
mode TEXT NOT NULL DEFAULT 'MONITOR' CHECK(mode IN('MONITOR','ENFORCE')),
default_action TEXT NOT NULL DEFAULT 'ALERT' CHECK(default_action IN('ALLOW','BLOCK','ALERT')),
version INTEGER NOT NULL DEFAULT 1 CHECK(version>=1),
created_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')),
updated_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')))""",
"""CREATE TABLE sensitive_data_types(
sensitive_type_id TEXT PRIMARY KEY, code TEXT NOT NULL UNIQUE, name TEXT NOT NULL,
description TEXT NOT NULL DEFAULT '', pattern TEXT, is_custom INTEGER NOT NULL DEFAULT 0 CHECK(is_custom IN(0,1)),
enabled INTEGER NOT NULL DEFAULT 1 CHECK(enabled IN(0,1)),
created_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')))""",
"""CREATE TABLE rules(
rule_id TEXT PRIMARY KEY, policy_id TEXT NOT NULL, name TEXT NOT NULL,
event_type TEXT NOT NULL DEFAULT '*', channel TEXT NOT NULL DEFAULT '*',
sensitive_type_id TEXT, source_pattern TEXT, destination_type TEXT, file_extension TEXT,
action TEXT NOT NULL CHECK(action IN('ALLOW','BLOCK','ALERT')),
priority INTEGER NOT NULL DEFAULT 100 CHECK(priority BETWEEN 1 AND 1000),
enabled INTEGER NOT NULL DEFAULT 1 CHECK(enabled IN(0,1)),
created_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')),
updated_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')),
FOREIGN KEY(policy_id) REFERENCES policies(policy_id) ON DELETE CASCADE,
FOREIGN KEY(sensitive_type_id) REFERENCES sensitive_data_types(sensitive_type_id) ON DELETE RESTRICT)""",
"""CREATE TABLE events(
event_id TEXT PRIMARY KEY, device_id TEXT, channel TEXT NOT NULL, event_type TEXT NOT NULL,
event_timestamp TEXT NOT NULL, findings_metadata TEXT NOT NULL DEFAULT '{}',
decision TEXT, policy_id TEXT, enforcement_status TEXT NOT NULL DEFAULT 'NOT_APPLIED'
CHECK(enforcement_status IN('NOT_APPLIED','APPLIED','FAILED','UNKNOWN')),
received_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')),
FOREIGN KEY(device_id) REFERENCES devices(device_id) ON DELETE SET NULL)""",
"""CREATE TABLE incidents(
incident_id TEXT PRIMARY KEY, event_id TEXT, title TEXT NOT NULL, description TEXT NOT NULL DEFAULT '',
severity TEXT NOT NULL CHECK(severity IN('LOW','MEDIUM','HIGH','CRITICAL')),
status TEXT NOT NULL DEFAULT 'OPEN' CHECK(status IN('OPEN','INVESTIGATING','RESOLVED','CLOSED')),
created_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')),
updated_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')), resolved_at TEXT,
FOREIGN KEY(event_id) REFERENCES events(event_id) ON DELETE SET NULL)""",
"""CREATE TABLE audit_logs(
audit_id TEXT PRIMARY KEY, admin_id TEXT, action TEXT NOT NULL, target_type TEXT NOT NULL,
target_id TEXT, details TEXT NOT NULL DEFAULT '{}',
created_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')),
FOREIGN KEY(admin_id) REFERENCES administrators(admin_id) ON DELETE SET NULL)""",
"CREATE INDEX idx_rules_policy_priority ON rules(policy_id,enabled,priority,created_at)",
"CREATE INDEX idx_events_device_time ON events(device_id,event_timestamp)",
"CREATE INDEX idx_incidents_status ON incidents(status,severity)",
"CREATE INDEX idx_audit_created ON audit_logs(created_at)"
]
