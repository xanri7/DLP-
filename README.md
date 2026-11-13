# NEON SENTINEL DLP — Phase 1
Python 3.10+. Standard library only.

Initialize: `python run.py init-db`
Test: `python -m unittest discover -s tests -v`

The database starts empty. Tests use isolated temporary databases.
This phase implements database, policies, rules, policy evaluation, event metadata,
device inventory, incidents, administrator authentication primitives and audit logs.
It does not implement Flask routes, browser UI, Agent communication, endpoint monitoring,
or actual enforcement. The policy engine evaluates structured metadata only; raw file
or clipboard contents are never accepted or stored.

Rule priority is ascending (1 is highest). First matching enabled rule wins.
If none matches, the policy's default action is returned.
