from sqlalchemy.orm import Session
from app.db.models import SourceFileState


class SourceFileStateRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_profile_and_path(self, source_profile_id: str, file_path: str) -> SourceFileState | None:
        return (
            self.db.query(SourceFileState)
            .filter(
                SourceFileState.source_profile_id == source_profile_id,
                SourceFileState.file_path == file_path,
            )
            .first()
        )

    def create(self, **kwargs) -> SourceFileState:
        item = SourceFileState(**kwargs)
        self.db.add(item)
        self.db.flush()
        return item

    def upsert(
        self,
        source_profile_id: str,
        file_path: str,
        size_bytes: int,
        mtime_ns: int,
        content_hash: str | None,
        last_document_id: str | None,
        last_seen_at: str,
        status: str,
    ) -> SourceFileState:
        existing = self.get_by_profile_and_path(source_profile_id=source_profile_id, file_path=file_path)
        if existing:
            existing.size_bytes = size_bytes
            existing.mtime_ns = mtime_ns
            existing.content_hash = content_hash
            existing.last_document_id = last_document_id
            existing.last_seen_at = last_seen_at
            existing.status = status
            self.db.flush()
            return existing
        return self.create(
            source_profile_id=source_profile_id,
            file_path=file_path,
            size_bytes=size_bytes,
            mtime_ns=mtime_ns,
            content_hash=content_hash,
            last_document_id=last_document_id,
            last_seen_at=last_seen_at,
            status=status,
        )

