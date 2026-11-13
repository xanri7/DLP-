import json
from server.database.connection import db
from server.validators import text,metadata
def record_event(event,db_path=None):
    if not isinstance(event,dict): raise ValueError("event must be dict")
    eid=text(event.get("event_id"),"event_id",120); ch=text(event.get("channel"),"channel",40)
    typ=text(event.get("event_type"),"event_type",80); ts=text(event.get("event_timestamp"),"event_timestamp",50)
    meta=metadata(event.get("findings_metadata",{})); decision=event.get("decision")
    if decision not in (None,"ALLOW","BLOCK","ALERT","NO_MATCH"): raise ValueError("Invalid decision")
    status=event.get("enforcement_status","NOT_APPLIED")
    if status not in ("NOT_APPLIED","APPLIED","FAILED","UNKNOWN"): raise ValueError("Invalid enforcement status")
    with db(db_path,True) as c:
        did=event.get("device_id")
        if did and not c.execute("SELECT 1 FROM devices WHERE device_id=?",(did,)).fetchone(): raise ValueError("Device not found")
        cur=c.execute("""INSERT INTO events(event_id,device_id,channel,event_type,event_timestamp,findings_metadata,decision,policy_id,enforcement_status)
        VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(event_id) DO NOTHING""",
        (eid,did,ch,typ,ts,json.dumps(meta),decision,event.get("policy_id"),status))
    return cur.rowcount==1
def list_events(limit=100,db_path=None):
    if type(limit) is not int or not 1<=limit<=500: raise ValueError("limit must be 1..500")
    with db(db_path) as c: rows=c.execute("SELECT * FROM events ORDER BY received_at DESC LIMIT ?",(limit,)).fetchall()
    out=[dict(r) for r in rows]
    for r in out: r["findings_metadata"]=json.loads(r["findings_metadata"])
    return out
