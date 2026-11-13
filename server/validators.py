import json, re
ACTIONS={"ALLOW","BLOCK","ALERT"}
MODES={"MONITOR","ENFORCE"}
def text(v, field, maxlen=200):
    if not isinstance(v,str) or not v.strip() or len(v.strip())>maxlen: raise ValueError(f"Invalid {field}")
    return v.strip()
def optional(v, field, maxlen=500):
    if v is None: return None
    if not isinstance(v,str) or len(v)>maxlen: raise ValueError(f"Invalid {field}")
    return v.strip() or None
def enum(v, choices, field):
    if v not in choices: raise ValueError(f"Invalid {field}")
    return v
def pattern(v):
    v=optional(v,"pattern",1000)
    if v:
        try: re.compile(v)
        except re.error as e: raise ValueError(f"Invalid regex: {e}") from e
    return v
def metadata(v):
    if v is None: v={}
    if not isinstance(v,dict): raise ValueError("Metadata must be a dictionary")
    allowed={"file_extension","file_size","source_type","destination_type","sensitive_types",
             "detection_count","matched_pattern_ids","clipboard_char_count","application",
             "process_name","mime_type","file_count","classification","source_pattern_id"}
    extra=set(v)-allowed
    if extra: raise ValueError(f"Unsupported metadata fields: {sorted(extra)}")
    for k in ("file_size","detection_count","clipboard_char_count","file_count"):
        if k in v and (type(v[k]) is not int or v[k]<0): raise ValueError(f"Invalid {k}")
    for k in ("sensitive_types","matched_pattern_ids"):
        if k in v and (not isinstance(v[k],list) or not all(isinstance(x,str) for x in v[k])):
            raise ValueError(f"Invalid {k}")
    json.dumps(v)
    return v
