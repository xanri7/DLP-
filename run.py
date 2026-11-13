import argparse, os
from server.database.connection import initialize_database
p=argparse.ArgumentParser()
p.add_argument("command", choices=["init-db"])
a=p.parse_args()
initialize_database(os.environ.get("NEON_DB_PATH"))
print("NEON SENTINEL database initialized.")
