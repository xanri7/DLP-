from uuid import uuid4
from server.database.connection import db
from server.validators import text, optional, enum, ACTIONS, MODES
def create_policy(name,description="",mode="MONITOR",default_action="ALERT",db_path=None):
    pid=str(uuid4()); name=text(name,"name",100); description=optional(description,"description",1000) or ""
    enum(mode,MODES,"mode"); enum(default_action,ACTIONS,"default_action")
    with db(db_path,True) as c:
        c.execute("INSERT INTO policies(policy_id,name,description,mode,default_action) VALUES(?,?,?,?,?)",
                  (pid,name,description,mode,default_action))
    return pid
def get_policy(pid,db_path=None):
    with db(db_path) as c: r=c.execute("SELECT * FROM policies WHERE policy_id=?",(pid,)).fetchone()
    return dict(r) if r else None
def get_policies(db_path=None):
    with db(db_path) as c: rows=c.execute("SELECT * FROM policies ORDER BY updated_at DESC,policy_id").fetchall()
    return [dict(r) for r in rows]
def update_policy(pid,db_path=None,**changes):
    allowed={"name","description","mode","default_action"}
    if not changes or set(changes)-allowed: raise ValueError("No valid policy fields")
    if "name" in changes: changes["name"]=text(changes["name"],"name",100)
    if "description" in changes: changes["description"]=optional(changes["description"],"description",1000) or ""
    if "mode" in changes: enum(changes["mode"],MODES,"mode")
    if "default_action" in changes: enum(changes["default_action"],ACTIONS,"default_action")
    cols=",".join(f"{k}=?" for k in changes)
    with db(db_path,True) as c:
        cur=c.execute(f"UPDATE policies SET {cols},version=version+1,updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE policy_id=?",(*changes.values(),pid))
        if cur.rowcount!=1: raise ValueError("Policy not found")
    return get_policy(pid,db_path)
def set_policy_enabled(pid,enabled,db_path=None):
    if type(enabled) is not bool: raise ValueError("enabled must be bool")
    with db(db_path,True) as c:
        cur=c.execute("UPDATE policies SET enabled=?,version=version+1,updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE policy_id=?",(int(enabled),pid))
        if cur.rowcount!=1: raise ValueError("Policy not found")
    return get_policy(pid,db_path)
def delete_policy(pid,db_path=None):
    with db(db_path,True) as c:
        cur=c.execute("DELETE FROM policies WHERE policy_id=?",(pid,))
        if cur.rowcount!=1: raise ValueError("Policy not found")
    return True
def get_policy_bundle(pid,db_path=None):
    with db(db_path) as c:
        p=c.execute("SELECT policy_id,name,mode,default_action,enabled,version FROM policies WHERE policy_id=? AND enabled=1",(pid,)).fetchone()
        if not p: return None
        rs=c.execute("SELECT * FROM rules WHERE policy_id=? AND enabled=1 ORDER BY priority,created_at,rule_id",(pid,)).fetchall()
    out=dict(p); out["rules"]=[dict(r) for r in rs]; return out
