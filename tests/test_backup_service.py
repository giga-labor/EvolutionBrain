import os
import shutil
import tempfile
import pytest

from app.platform.backup_service import BackupService


@pytest.fixture
def tmp_db(tmp_path):
    import sqlite3
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute("CREATE TABLE marker (val TEXT)")
    conn.execute("INSERT INTO marker VALUES ('original')")
    conn.commit()
    conn.close()
    return str(db_file)


@pytest.fixture
def backup_svc(tmp_db):
    return BackupService(f"sqlite:///{tmp_db}")


class TestBackupService:
    def test_create_backup_produces_file(self, backup_svc, tmp_db):
        backup_path = backup_svc.create_backup()
        assert os.path.exists(backup_path)
        assert "evobrain_" in os.path.basename(backup_path)
        assert backup_path.endswith(".sqlite")

    def test_create_backup_in_backups_subdir(self, backup_svc, tmp_db):
        backup_path = backup_svc.create_backup()
        parent_dir = os.path.dirname(backup_path)
        assert os.path.basename(parent_dir) == "backups"

    def test_multiple_backups_unique_names(self, backup_svc):
        import time
        path1 = backup_svc.create_backup()
        time.sleep(1.1)  # Ensure different timestamp
        path2 = backup_svc.create_backup()
        assert path1 != path2

    def test_restore_backup_overwrites_db(self, backup_svc, tmp_db):
        import sqlite3
        backup_path = backup_svc.create_backup()
        # Overwrite original with different data
        conn = sqlite3.connect(tmp_db)
        conn.execute("DELETE FROM marker")
        conn.execute("INSERT INTO marker VALUES ('modified')")
        conn.commit()
        conn.close()
        # Restore from backup
        restored = backup_svc.restore_backup(backup_path)
        assert restored == tmp_db
        # Verify original data was restored
        conn = sqlite3.connect(tmp_db)
        val = conn.execute("SELECT val FROM marker").fetchone()[0]
        conn.close()
        assert val == "original"

    def test_create_backup_missing_db_raises(self, tmp_path):
        svc = BackupService(f"sqlite:///{tmp_path}/nonexistent.db")
        with pytest.raises(FileNotFoundError):
            svc.create_backup()

    def test_restore_missing_backup_raises(self, backup_svc):
        with pytest.raises(FileNotFoundError):
            backup_svc.restore_backup("/nonexistent/path/backup.sqlite")
