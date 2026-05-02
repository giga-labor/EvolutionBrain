import os
import shutil
from datetime import datetime, UTC


class BackupService:
    def __init__(self, db_url: str, retention_count: int = 20):
        self.db_url = db_url
        self.retention_count = max(1, int(retention_count))

    def _db_path(self) -> str:
        if "///" not in self.db_url:
            raise ValueError("Unsupported database URL for backup service")
        return self.db_url.split("///", 1)[1]

    def create_backup(self) -> str:
        import sqlite3
        db_path = self._db_path()
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
        backup_dir = os.path.join(os.path.dirname(db_path), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"evobrain_{ts}.sqlite")
        src = sqlite3.connect(db_path)
        dst = sqlite3.connect(backup_path)
        try:
            src.backup(dst)
        finally:
            src.close()
            dst.close()
        self._enforce_retention(backup_dir)
        return backup_path

    def _enforce_retention(self, backup_dir: str) -> None:
        files = [
            os.path.join(backup_dir, name)
            for name in os.listdir(backup_dir)
            if name.startswith("evobrain_") and name.endswith(".sqlite")
        ]
        files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        for old_path in files[self.retention_count:]:
            try:
                os.remove(old_path)
            except OSError:
                # Best effort: backup creation should not fail due to cleanup errors.
                pass

    def restore_backup(self, backup_path: str) -> str:
        import sqlite3
        db_path = self._db_path()
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        # Use SQLite backup API so the file lock held by SQLAlchemy is not a problem
        src = sqlite3.connect(backup_path)
        dst = sqlite3.connect(db_path)
        try:
            src.backup(dst)
        finally:
            src.close()
            dst.close()
        return db_path
