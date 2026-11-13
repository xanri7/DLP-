from .schema import VERSION, DDL
def migrate(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT(strftime('%Y-%m-%dT%H:%M:%fZ','now')))")
    current=conn.execute("SELECT COALESCE(MAX(version),0) FROM schema_migrations").fetchone()[0]
    if current>VERSION: raise RuntimeError("Database schema is newer than this application")
    if current<1:
        for sql in DDL: conn.execute(sql)
        conn.execute("INSERT INTO schema_migrations(version) VALUES(1)")
