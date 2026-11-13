from uuid import uuid4
from server.database.connection import db
from server.validators import text, optional, enum, pattern, ACTIONS
def create_sensitive_type(code,name,description="",regex=None,is_custom=True,db_path=None):
    code=text(code,"code",60).upper()
    if not code.replace("_","").isalnum(): raise ValueError("Invalid type code")
    name=text(name,"name",100); description=optional(description,"description",500) or ""; regex=pattern(regex)
    if type(is_custom) is not bool: raise ValueError("is_custom must be bool")
    sid=str(uuid4())
    with db(db_path,True) as c:
        c.execute("INSERT INTO sensitive_data_types(sensitive_type_id,code,name,description,pattern,is_custom) VALUES(?,?,?,?,?,?)",
                  (sid,code,name,description,regex,int(is_custom)))
    return sid
def list_sensitive_types(db_path=None):
    with db(db_path) as c: rows=c.execute("SELECT * FROM sensitive_data_types ORDER BY code").fetchall()
    return [dict(r) for r in rows]
def create_rule(pid,name,action,event_type="*",channel="*",*,sensitive_type_id=None,source_pattern=None,destination_type=None,file_extension=None,priority=100,enabled=True,db_path=None):
    name=text(name,"name",100); enum(action,ACTIONS,"action"); event_type=text(event_type,"event_type",80); channel=text(channel,"channel",40)
    source_pattern=pattern(source_pattern); destination_type=optional(destination_type,"destination_type",80)
    file_extension=optional(file_extension,"file_extension",20)
    if file_extension: file_extension=file_extension.lower().lstrip(".")
    if type(priority) is not int or not 1<=priority<=1000: raise ValueError("priority must be 1..1000")
    if type(enabled) is not bool: raise ValueError("enabled must be bool")
    rid=str(uuid4())
    with db(db_path,True) as c:
        if not c.execute("SELECT 1 FROM policies WHERE policy_id=?",(pid,)).fetchone(): raise ValueError("Policy not found")
        if sensitive_type_id and not c.execute("SELECT 1 FROM sensitive_data_types WHERE sensitive_type_id=? AND enabled=1",(sensitive_type_id,)).fetchone(): raise ValueError("Sensitive type missing/disabled")
        c.execute("""INSERT INTO rules(rule_id,policy_id,name,event_type,channel,sensitive_type_id,source_pattern,destination_type,file_extension,action,priority,enabled)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",(rid,pid,name,event_type,channel,sensitive_type_id,source_pattern,destination_type,file_extension,action,priority,int(enabled)))
        c.execute("UPDATE policies SET version=version+1,updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE policy_id=?",(pid,))
    return rid
def list_rules(pid=None,db_path=None):
    with db(db_path) as c:
        q="SELECT * FROM rules"; args=()
        if pid: q+=" WHERE policy_id=?"; args=(pid,)
        rows=c.execute(q+" ORDER BY priority,created_at,rule_id",args).fetchall()
    return [dict(r) for r in rows]
def update_rule(rid,db_path=None,**changes):
    allowed={"name","event_type","channel","source_pattern","destination_type","file_extension","action","priority","enabled","sensitive_type_id"}
    if not changes or set(changes)-allowed: raise ValueError("Invalid rule changes")
    if "name" in changes: changes["name"]=text(changes["name"],"name",100)
    if "event_type" in changes: changes["event_type"]=text(changes["event_type"],"event_type",80)
    if "channel" in changes: changes["channel"]=text(changes["channel"],"channel",40)
    if "action" in changes: enum(changes["action"],ACTIONS,"action")
    if "source_pattern" in changes: changes["source_pattern"]=pattern(changes["source_pattern"])
    for k in ("destination_type","file_extension"):
        if k in changes: changes[k]=optional(changes[k],k,80 if k=="destination_type" else 20)
    if changes.get("file_extension"): changes["file_extension"]=changes["file_extension"].lower().lstrip(".")
    if "priority" in changes and (type(changes["priority"]) is not int or not 1<=changes["priority"]<=1000): raise ValueError("priority must be 1..1000")
    if "enabled" in changes and type(changes["enabled"]) is not bool: raise ValueError("enabled must be bool")
    with db(db_path,True) as c:
        row=c.execute("SELECT policy_id FROM rules WHERE rule_id=?",(rid,)).fetchone()
        if not row: raise ValueError("Rule not found")
        cols=",".join(f"{k}=?" for k in changes); vals=[int(v) if isinstance(v,bool) else v for v in changes.values()]
        c.execute(f"UPDATE rules SET {cols},updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE rule_id=?",(*vals,rid))
        c.execute("UPDATE policies SET version=version+1,updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE policy_id=?",(row["policy_id"],))
    return True
def delete_rule(rid,db_path=None):
    with db(db_path,True) as c:
        row=c.execute("SELECT policy_id FROM rules WHERE rule_id=?",(rid,)).fetchone()
        if not row: raise ValueError("Rule not found")
        c.execute("DELETE FROM rules WHERE rule_id=?",(rid,))
        c.execute("UPDATE policies SET version=version+1,updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE policy_id=?",(row["policy_id"],))
    return True
