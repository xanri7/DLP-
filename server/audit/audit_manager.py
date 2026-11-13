import json
from uuid import uuid4
from server.database.connection import db
from server.validators import text
def record_audit(action,target_type,target_id=None,admin_id=None,details=None,db_path=None):
    action=text(action,"action",100); target_type=text(target_type,"target_type",100)
    if details is None: details={}
    if not isinstance(details,dict): raise ValueError("details must be a dictionary")
    aid=str(uuid4())
    with db(db_path,True) as c:
        c.execute("INSERT INTO audit_logs(audit_id,admin_id,action,target_type,target_id,details) VALUES(?,?,?,?,?,?)",
                  (aid,admin_id,action,target_type,target_id,json.dumps(details)))
    return aid
