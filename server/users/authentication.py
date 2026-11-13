import os,hashlib,hmac
from uuid import uuid4
from server.database.connection import db
from server.validators import text
def _hash(password,salt):
    if not isinstance(password,str) or len(password)<12: raise ValueError("Password must be at least 12 characters")
    return hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1).hex()
def create_first_admin(username,password,db_path=None):
    username=text(username,"username",80)
    if any(c.isspace() for c in username): raise ValueError("Username cannot contain spaces")
    salt=os.urandom(16); digest=_hash(password,salt); aid=str(uuid4())
    with db(db_path,True) as c:
        if c.execute("SELECT COUNT(*) FROM administrators").fetchone()[0]: raise ValueError("Administrator already exists")
        c.execute("INSERT INTO administrators(admin_id,username,password_hash,password_salt) VALUES(?,?,?,?)",(aid,username,digest,salt.hex()))
    return aid
def authenticate(username,password,db_path=None):
    if not isinstance(username,str) or not isinstance(password,str): return None
    with db(db_path) as c: r=c.execute("SELECT * FROM administrators WHERE username=? COLLATE NOCASE",(username.strip(),)).fetchone()
    if not r or not r["is_active"]: return None
    try: candidate=_hash(password,bytes.fromhex(r["password_salt"]))
    except ValueError: return None
    if not hmac.compare_digest(candidate,r["password_hash"]): return None
    with db(db_path,True) as c: c.execute("UPDATE administrators SET last_login_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE admin_id=?",(r["admin_id"],))
    return {"admin_id":r["admin_id"],"username":r["username"]}
