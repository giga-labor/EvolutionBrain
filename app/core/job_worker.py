import asyncio
import logging
from datetime import datetime, timezone

logger = logging.getLogger("evobrain.job_worker")

MAX_RETRIES = 3
POLL_INTERVAL = 10  # seconds between queue polls


class JobWorker:
    async def run(self):
        logger.info("Job worker started")
        while True:
            try:
                await self._process_one()
            except asyncio.CancelledError:
                logger.info("Job worker stopped")
                return
            except Exception as exc:
                logger.error("Job worker error: %s", exc)
            await asyncio.sleep(POLL_INTERVAL)

    async def _process_one(self):
        from app.db.session import SessionLocal
        with SessionLocal() as db:
            job = self._next_queued_job(db)
            if not job:
                return
            self._mark(db, job, "running")
            try:
                self._dispatch(db, job)
                self._mark(db, job, "completed")
                logger.info("Job %s (%s) completed", job.id, job.job_type)
            except Exception as exc:
                logger.warning("Job %s failed: %s", job.id, exc)
                job.retry_count = (job.retry_count or 0) + 1
                db.commit()
                if job.retry_count >= MAX_RETRIES:
                    self._mark(db, job, "failed")
                else:
                    self._mark(db, job, "queued")

    @staticmethod
    def _next_queued_job(db):
        from app.db.models import Job
        return (
            db.query(Job)
            .filter(Job.status == "queued")
            .order_by(Job.priority.desc())
            .first()
        )

    @staticmethod
    def _mark(db, job, status: str):
        job.status = status
        db.commit()

    def _dispatch(self, db, job):
        if job.job_type == "ingest_document":
            self._process_ingest_documents(db)
        elif job.job_type == "normalize_document":
            self._process_normalize_documents(db)
        elif job.job_type == "index_document":
            self._process_index_documents(db)

    @staticmethod
    def _process_ingest_documents(db):
        from app.db.models import Document
        from app.audit.service import AuditService
        docs = (
            db.query(Document)
            .filter(Document.ingestion_status == "raw_pending")
            .all()
        )
        audit = AuditService(db)
        for doc in docs:
            content = doc.raw_content or ""
            if doc.title and not doc.title.strip():
                doc.title = doc.title.strip()
            doc.ingestion_status = "completed"
            doc.normalization_status = "completed"
            audit.log("document", doc.id, "job.ingest_completed",
                      {"content_length": len(content)})
        db.commit()
        logger.info("Ingested %d documents", len(docs))

    @staticmethod
    def _process_normalize_documents(db):
        from app.db.models import Document
        docs = (
            db.query(Document)
            .filter(Document.normalization_status == "pending")
            .all()
        )
        for doc in docs:
            doc.normalization_status = "completed"
        db.commit()

    @staticmethod
    def _process_index_documents(db):
        from app.db.models import Document
        docs = (
            db.query(Document)
            .filter(Document.semantic_status == "pending")
            .all()
        )
        for doc in docs:
            doc.semantic_status = "indexed"
        db.commit()
