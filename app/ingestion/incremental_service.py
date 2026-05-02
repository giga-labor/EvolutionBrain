import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy.orm import Session

from app.audit.service import AuditService
from app.db.repositories.source_file_state import SourceFileStateRepo
from app.ingestion.service import IngestionService


class IncrementalIngestionService:
    _TEXT_EXTENSIONS = {
        ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".kt", ".go", ".rs", ".c", ".h", ".cpp", ".hpp", ".cs",
        ".html", ".css", ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".xml", ".csv", ".tsv", ".log",
        ".ini", ".cfg", ".toml", ".ps1", ".bat", ".sh", ".sql", ".help", ".svg",
    }
    _DB_EXTENSIONS = {".db", ".sqlite", ".sqlite3"}
    _NEURAL_EXTENSIONS = {".pt", ".pth", ".ckpt", ".h5", ".hdf5", ".onnx", ".npy", ".npz"}
    _NEURAL_PATH_MARKERS = (
        "\\checkpoints\\",
        "\\super6_nn\\runs\\",
        "\\spotlight\\neurali\\",
        "\\paradox_engine\\models\\",
        "\\src\\models\\",
        "\\weights\\",
    )

    def __init__(self, db: Session):
        self.db = db
        self.ingestion = IngestionService(db)
        self.state_repo = SourceFileStateRepo(db)
        self.audit = AuditService(db)

    @classmethod
    def _is_neural_archive(cls, file_path: Path) -> bool:
        low = str(file_path).lower()
        if file_path.suffix.lower() in cls._NEURAL_EXTENSIONS:
            return True
        if any(marker in low for marker in cls._NEURAL_PATH_MARKERS):
            return True
        if file_path.suffix.lower() == ".bin" and ("geneticse" in low or "super6" in low or "neur" in low):
            return True
        return False

    @classmethod
    def _is_supported(cls, file_path: Path) -> bool:
        ext = file_path.suffix.lower()
        return ext in cls._TEXT_EXTENSIONS or ext in cls._DB_EXTENSIONS

    @staticmethod
    def _sha256(data: str) -> str:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @staticmethod
    def _sqlite_summary(path: Path) -> str:
        lines: list[str] = [
            f"DB Summary: {path.name}",
            f"Path: {path}",
        ]
        con = sqlite3.connect(path)
        cur = con.cursor()
        cur.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table','view') ORDER BY type, name")
        objects = cur.fetchall()
        lines.append(f"Objects: {len(objects)}")
        for name, obj_type in objects[:200]:
            lines.append(f"- {obj_type}: {name}")
            if obj_type == "table" and not name.startswith("sqlite_"):
                try:
                    cur.execute(f"SELECT COUNT(*) FROM [{name}]")
                    rows = cur.fetchone()[0]
                    lines.append(f"  rows={rows}")
                except Exception:
                    lines.append("  rows=ERR")
        con.close()
        return "\n".join(lines)

    def sync_source_updates(self, source_profile_id: str, source_path: str) -> dict:
        root = Path(source_path)
        if not root.exists() or not root.is_dir():
            return {"ok": False, "error": f"source path not found: {source_path}"}

        now_iso = datetime.now(timezone.utc).isoformat()
        stats = {
            "files_seen": 0,
            "supported_candidates": 0,
            "neural_excluded": 0,
            "unchanged_skipped": 0,
            "updated_processed": 0,
            "created": 0,
            "duplicate": 0,
            "errors": 0,
            "db_summaries": 0,
        }

        for path in root.rglob("*"):
            if not path.is_file():
                continue
            stats["files_seen"] += 1

            if self._is_neural_archive(path):
                stats["neural_excluded"] += 1
                continue
            if not self._is_supported(path):
                continue

            stats["supported_candidates"] += 1
            rel = str(path.relative_to(root))
            try:
                st = path.stat()
                size_bytes = int(st.st_size)
                mtime_ns = int(st.st_mtime_ns)
            except Exception:
                stats["errors"] += 1
                continue

            prev = self.state_repo.get_by_profile_and_path(source_profile_id=source_profile_id, file_path=rel)
            if prev and prev.size_bytes == size_bytes and prev.mtime_ns == mtime_ns:
                self.state_repo.upsert(
                    source_profile_id=source_profile_id,
                    file_path=rel,
                    size_bytes=size_bytes,
                    mtime_ns=mtime_ns,
                    content_hash=prev.content_hash,
                    last_document_id=prev.last_document_id,
                    last_seen_at=now_iso,
                    status=prev.status,
                )
                stats["unchanged_skipped"] += 1
                continue

            try:
                ext = path.suffix.lower()
                if ext in self._DB_EXTENSIONS:
                    content = self._sqlite_summary(path)
                    source_type = "db_schema"
                    title = f"[DB] {rel}"
                    stats["db_summaries"] += 1
                else:
                    try:
                        content = path.read_text(encoding="utf-8")
                    except UnicodeDecodeError:
                        content = path.read_text(encoding="utf-8", errors="ignore")
                    if not content.strip():
                        self.state_repo.upsert(
                            source_profile_id=source_profile_id,
                            file_path=rel,
                            size_bytes=size_bytes,
                            mtime_ns=mtime_ns,
                            content_hash=None,
                            last_document_id=None,
                            last_seen_at=now_iso,
                            status="empty",
                        )
                        stats["updated_processed"] += 1
                        continue
                    source_type = "file"
                    title = rel

                result = self.ingestion.import_text(
                    content=content,
                    title=title,
                    source_type=source_type,
                    source_ref=str(path),
                )

                doc_id = result.get("document_id")
                status = result.get("status", "unknown")
                if status == "created":
                    stats["created"] += 1
                elif status == "duplicate":
                    stats["duplicate"] += 1
                stats["updated_processed"] += 1

                self.state_repo.upsert(
                    source_profile_id=source_profile_id,
                    file_path=rel,
                    size_bytes=size_bytes,
                    mtime_ns=mtime_ns,
                    content_hash=self._sha256(content),
                    last_document_id=doc_id,
                    last_seen_at=now_iso,
                    status=status,
                )
            except Exception:
                stats["errors"] += 1
                self.state_repo.upsert(
                    source_profile_id=source_profile_id,
                    file_path=rel,
                    size_bytes=size_bytes,
                    mtime_ns=mtime_ns,
                    content_hash=prev.content_hash if prev else None,
                    last_document_id=prev.last_document_id if prev else None,
                    last_seen_at=now_iso,
                    status="error",
                )

        self.db.commit()
        self.audit.log(
            "source_profile",
            source_profile_id,
            "incremental_sync_updates",
            {"source_path": source_path, **stats},
        )
        return {"ok": True, **stats}

