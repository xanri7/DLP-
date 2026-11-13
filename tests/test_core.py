import tempfile,unittest
from pathlib import Path
from server.database.connection import initialize_database,db
from server.policies.policy_manager import create_policy,get_policy,update_policy,set_policy_enabled,delete_policy
from server.policies.rule_manager import create_rule,update_rule,delete_rule
from server.policies.policy_engine import evaluate_event
from server.users.authentication import create_first_admin,authenticate
from server.events.event_manager import record_event
class CoreTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.path=str(Path(self.tmp.name)/"t.db"); initialize_database(self.path)
 def tearDown(self): self.tmp.cleanup()
 def test_empty_schema(self):
  with db(self.path) as c:
   self.assertEqual(c.execute("SELECT COUNT(*) FROM policies").fetchone()[0],0)
   self.assertEqual(c.execute("PRAGMA foreign_keys").fetchone()[0],1)
 def test_policy_rule_versions(self):
  p=create_policy("Protect",db_path=self.path); self.assertEqual(get_policy(p,self.path)["version"],1)
  r=create_rule(p,"Block PDF","BLOCK","FILE_COPY","FILE",file_extension="pdf",priority=2,db_path=self.path)
  self.assertEqual(get_policy(p,self.path)["version"],2)
  result=evaluate_event(p,{"event_type":"FILE_COPY","channel":"FILE","findings_metadata":{"file_extension":"pdf"}},self.path)
  self.assertEqual(result["decision"],"BLOCK")
  update_rule(r,priority=1,db_path=self.path); self.assertEqual(get_policy(p,self.path)["version"],3)
  delete_rule(r,self.path); self.assertEqual(get_policy(p,self.path)["version"],4)
  update_policy(p,mode="ENFORCE",db_path=self.path); self.assertEqual(get_policy(p,self.path)["version"],5)
  set_policy_enabled(p,False,self.path); self.assertIsNone(evaluate_event(p,{"event_type":"X","channel":"FILE"},self.path)["policy_version"])
  delete_policy(p,self.path); self.assertIsNone(get_policy(p,self.path))
 def test_authentication(self):
  aid=create_first_admin("admin","Strong-password-2026",self.path)
  self.assertEqual(authenticate("ADMIN","Strong-password-2026",self.path)["admin_id"],aid)
  self.assertIsNone(authenticate("admin","wrong-password",self.path))
  with self.assertRaises(ValueError): create_first_admin("other","Strong-password-2026",self.path)
 def test_no_raw_event_content(self):
  with self.assertRaises(ValueError):
   record_event({"event_id":"x","channel":"CLIPBOARD","event_type":"COPY","event_timestamp":"now","findings_metadata":{"clipboard_text":"secret"}},self.path)
if __name__=="__main__": unittest.main()
