"""SQLite persistence for normalized DLP events."""
import json
import os
import sqlite3
from pathlib import Path

class EventRepository:
    def __init__(self, path=None):
        self.path = Path(path or os.getenv("DLP_EVENT_DB", "server/data/events.sqlite3"))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute("""CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                channel TEXT NOT NULL,
                decision TEXT NOT NULL,
                payload TEXT NOT NULL
            )""")

    def _connect(self):
        return sqlite3.connect(self.path)

    def add(self, event):
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO events VALUES (?, ?, ?, ?, ?)",
                (event["event_id"], event["timestamp"], event["channel"],
                 event["decision"], json.dumps(event))
            )

    def list_recent(self, limit=100):
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT payload FROM events ORDER BY timestamp DESC LIMIT ?", (limit,)
            ).fetchall()
        return [json.loads(row[0]) for row in rows]
