import os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DB_PATH=Path(os.environ.get("NEON_DB_PATH", ROOT/"data"/"neon_sentinel.db"))
