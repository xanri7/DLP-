from uuid import uuid4
from server.database.connection import db
from server.validators import text,optional
SEVERITIES={"LOW","MEDIUM","HIGH","CRITICAL"}; STATUSES={"OPEN","INVESTIGATING","RESOLVED","CLOSED"}
def create_incident(title,severity,description="",event_id=None,db_path=None):
    title=text(title,"title",200); description=optional(description,"description",2000) or ""
    if severity not in SEVERITIES: raise ValueError("Invalid severity")
    iid=str(uuid4())
    with db(db_path,True) as c:
        if event_id and not c.execute("SELECT 1 FROM events WHERE event_id=?",(event_id,)).fetchone(): raise ValueError("Event not found")
        c.execute("INSERT INTO incidents(incident_id,event_id,title,description,severity) VALUES(?,?,?,?,?)",(iid,event_id,title,description,severity))
    return iid
def update_incident(iid,status=None,severity=None,db_path=None):
    if status is None and severity is None: raise ValueError("No changes supplied")
    if status is not None and status not in STATUSES: raise ValueError("Invalid status")
    if severity is not None and severity not in SEVERITIES: raise ValueError("Invalid severity")
    changes={k:v for k,v in {"status":status,"severity":severity}.items() if v is not None}
    cols=",".join(f"{k}=?" for k in changes)
    with db(db_path,True) as c:
        cur=c.execute(f"UPDATE incidents SET {cols},updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE incident_id=?",(*changes.values(),iid))
        if cur.rowcount!=1: raise ValueError("Incident not found")
