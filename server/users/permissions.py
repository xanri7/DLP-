def require_admin(identity):
    if not isinstance(identity,dict) or not identity.get("admin_id"): raise PermissionError("Administrator login required")
    return True
