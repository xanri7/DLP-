import re
from server.database.connection import db
from server.policies.policy_manager import get_policy_bundle
from server.validators import metadata
def evaluate_event(pid,event,db_path=None):
    if not isinstance(event,dict): raise ValueError("event must be dict")
    for k in ("event_type","channel"):
        if not isinstance(event.get(k),str) or not event[k].strip(): raise ValueError(f"{k} required")
    meta=metadata(event.get("findings_metadata",{})); bundle=get_policy_bundle(pid,db_path)
    if not bundle: return {"decision":"NO_MATCH","reason":"POLICY_NOT_FOUND_OR_DISABLED","matched_rule_id":None,"policy_version":None,"enforcement_required":False}
    for r in bundle["rules"]:
        if r["event_type"]!="*" and r["event_type"].casefold()!=event["event_type"].casefold(): continue
        if r["channel"]!="*" and r["channel"].casefold()!=event["channel"].casefold(): continue
        if r["file_extension"] and r["file_extension"].lower().lstrip(".")!=str(meta.get("file_extension","")).lower().lstrip("."): continue
        if r["destination_type"] and r["destination_type"].casefold()!=str(meta.get("destination_type","")).casefold(): continue
        if r["sensitive_type_id"]:
            with db(db_path) as c: s=c.execute("SELECT code FROM sensitive_data_types WHERE sensitive_type_id=? AND enabled=1",(r["sensitive_type_id"],)).fetchone()
            if not s or s["code"] not in meta.get("sensitive_types",[]): continue
        if r["source_pattern"] and not re.search(r["source_pattern"],str(meta.get("source_pattern_id",""))): continue
        return {"decision":r["action"],"reason":"RULE_MATCH","matched_rule_id":r["rule_id"],"policy_version":bundle["version"],"mode":bundle["mode"],"enforcement_required":bundle["mode"]=="ENFORCE" and r["action"]=="BLOCK"}
    action=bundle["default_action"]
    return {"decision":action,"reason":"NO_RULE_MATCH","matched_rule_id":None,"policy_version":bundle["version"],"mode":bundle["mode"],"enforcement_required":bundle["mode"]=="ENFORCE" and action=="BLOCK"}
