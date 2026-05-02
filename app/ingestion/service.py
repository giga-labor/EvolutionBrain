import hashlib
from sqlalchemy.orm import Session
from app.db.repositories.documents import DocumentRepo
from app.db.repositories.jobs import JobRepo
from app.audit.service import AuditService


class IngestionService:
    def __init__(self, db: Session):
        self.doc_repo = DocumentRepo(db)
        self.job_repo = JobRepo(db)
        self.audit = AuditService(db)

    def import_text(
        self,
        content: str,
        title: str | None = None,
        source_type: str = "text",
        source_ref: str | None = None,
    ) -> dict:
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        existing = self.doc_repo.get_by_hash(content_hash)
        if existing:
            return {
                "document_id": existing.id,
                "job_id": None,
                "status": "duplicate",
                "title": existing.title,
                "content_length": len(content),
            }

        doc = self.doc_repo.create(
            source_type=source_type,
            source_ref=source_ref,
            title=title,
            content_hash=content_hash,
            raw_content=content,
            ingestion_status="raw_pending",
            normalization_status="pending",
            semantic_status="pending",
            validation_status="unvalidated",
        )

        job = self.job_repo.create(job_type="ingest_document", priority=0.5)

        self.audit.log(
            "document",
            doc.id,
            "import",
            {
                "title": title,
                "source_type": source_type,
                "source_ref": source_ref,
                "content_length": len(content),
            },
        )

        return {
            "document_id": doc.id,
            "job_id": job.id,
            "status": "created",
            "title": doc.title,
            "content_length": len(content),
        }
