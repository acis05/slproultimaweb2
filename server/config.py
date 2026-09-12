from pathlib import Path
import json, os, sys

BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
WEB_MODE = os.environ.get("STOKLEDGER_WEB_MODE", "1") == "1"
IS_RAILWAY = bool(os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("RAILWAY_PROJECT_ID"))
DATABASE_URL = str(os.environ.get("DATABASE_URL", "")).strip()
DATABASE_BACKEND = "postgresql" if DATABASE_URL else "sqlite"
IS_POSTGRES = DATABASE_BACKEND == "postgresql"

# PostgreSQL stores application records in Railway Postgres. Local directories are
# still used for logs/temp exports; project-document bytes are stored in PostgreSQL.
# SQLite fallback remains available for local compatibility when DATABASE_URL is absent.
if IS_POSTGRES:
    # No Railway Volume is required for database records in PostgreSQL mode.
    persistent_root = Path(os.environ.get("STOKLEDGER_PERSISTENT_ROOT", BASE_DIR))
elif IS_RAILWAY and not os.environ.get("STOKLEDGER_DATA_DIR"):
    persistent_root = Path(os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", "/data"))
else:
    persistent_root = Path(os.environ.get("STOKLEDGER_PERSISTENT_ROOT", BASE_DIR))

DATA_DIR = Path(os.environ.get("STOKLEDGER_DATA_DIR", (persistent_root / "data") if IS_POSTGRES else (persistent_root if IS_RAILWAY else persistent_root / "data")))
LOG_DIR = Path(os.environ.get("STOKLEDGER_LOG_DIR", DATA_DIR / "logs" if IS_RAILWAY else persistent_root / "logs"))
BACKUP_DIR = Path(os.environ.get("STOKLEDGER_BACKUP_DIR", DATA_DIR / "backups" if IS_RAILWAY else persistent_root / "backups"))
SELECTION_FILE = persistent_root / "database_selection.json"

def _selected_database_from_settings():
    if WEB_MODE:
        return None
    try:
        data = json.loads(SELECTION_FILE.read_text(encoding="utf-8"))
        value = str(data.get("database_path", "")).strip()
        if not value:
            return None
        candidate = Path(value).expanduser().resolve()
        return candidate if candidate.is_file() else None
    except Exception:
        return None

_env_database = str(os.environ.get("STOKLEDGER_DB_PATH", "")).strip()
_explicit = os.environ.get("STOKLEDGER_DATABASE_EXPLICIT") == "1"
if _explicit and not _env_database:
    raise RuntimeError("STOKLEDGER_DATABASE_EXPLICIT=1 tetapi STOKLEDGER_DB_PATH kosong.")

default_db = DATA_DIR / ("stokledger_pro_ultima_web.db" if WEB_MODE else "stokledger_pro_ultima.db")
DB_PATH = Path(_env_database).expanduser().resolve() if _env_database else (_selected_database_from_settings() or default_db)
HOST = os.environ.get("STOKLEDGER_HOST", "0.0.0.0")
# Railway injects PORT automatically.
PORT = int(os.environ.get("PORT", os.environ.get("STOKLEDGER_PORT", "8720")))
TOKEN_HOURS = int(os.environ.get("STOKLEDGER_TOKEN_HOURS", "8"))

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
