from server.database.connection import db
from server.validators import text
STATUSES={"PENDING","ONLINE","OFFLINE","DISABLED"}
def add_device(device_id,hostname,platform,status="PENDING",db_path=None):
    for v,k in ((device_id,"device_id"),(hostname,"hostname"),(platform,"platform")): text(v,k,120)
    if status not in STATUSES: raise ValueError("Invalid status")
    with db(db_path,True) as c: c.execute("INSERT INTO devices(device_id,hostname,platform,status) VALUES(?,?,?,?)",(device_id,hostname,platform,status))
    return device_id
def list_devices(db_path=None):
    with db(db_path) as c: rows=c.execute("SELECT * FROM devices ORDER BY registered_at DESC").fetchall()
    return [dict(r) for r in rows]
