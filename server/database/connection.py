import sqlite3
from pathlib import Path
from contextlib import contextmanager
from server.config import DB_PATH
from .migrations import migrate
def connect(path=None):
    p=Path(path) if path else DB_PATH
    p.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(str(p),timeout=10); c.row_factory=sqlite3.Row
    c.execute("PRAGMA foreign_keys=ON"); c.execute("PRAGMA busy_timeout=10000")
    return c
@contextmanager
def db(path=None, write=False):
    c=connect(path)
    try:
        if write: c.execute("BEGIN IMMEDIATE")
        yield c
        if write: c.commit()
    except Exception:
        if write: c.rollback()
        raise
    finally: c.close()
def initialize_database(path=None):
    with db(path,True) as c: migrate(c)
    return str(path or DB_PATH)
