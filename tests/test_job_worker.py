import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.repositories.jobs import JobRepo
from app.db.repositories.documents import DocumentRepo
from app.core.job_worker import JobWorker


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


def _make_job(db, job_type="ingest_document", priority=0.5):
    return JobRepo(db).create(job_type=job_type, status="queued", priority=priority)


def _make_doc(db, status="raw_pending"):
    return DocumentRepo(db).create(
        source_type="text",
        title="Test Doc",
        raw_content="Some content",
        content_hash="abc123",
        ingestion_status=status,
        normalization_status="pending",
        semantic_status="pending",
        validation_status="unvalidated",
    )


class TestJobWorker:
    def test_ingest_document_job_completes(self, db):
        doc = _make_doc(db)
        job = _make_job(db, "ingest_document")
        worker = JobWorker()
        worker._dispatch(db, job)
        worker._mark(db, job, "completed")
        refreshed_job = JobRepo(db).get(job.id)
        assert refreshed_job.status == "completed"
        refreshed_doc = DocumentRepo(db).get(doc.id)
        assert refreshed_doc.ingestion_status == "completed"

    def test_no_queued_jobs_does_nothing(self, db):
        # No jobs in queue - should not crash
        worker = JobWorker()
        job = worker._next_queued_job(db)
        assert job is None

    def test_highest_priority_processed_first(self, db):
        low = _make_job(db, priority=0.1)
        high = _make_job(db, priority=0.9)
        worker = JobWorker()
        next_job = worker._next_queued_job(db)
        assert next_job.id == high.id

    def test_completed_job_not_reprocessed(self, db):
        job = _make_job(db)
        JobRepo(db).update_status(job.id, "completed")
        worker = JobWorker()
        next_job = worker._next_queued_job(db)
        assert next_job is None

    def test_normalize_document_job(self, db):
        doc = _make_doc(db, status="completed")
        job = _make_job(db, "normalize_document")
        worker = JobWorker()
        worker._dispatch(db, job)
        refreshed = DocumentRepo(db).get(doc.id)
        assert refreshed.normalization_status == "completed"

    def test_index_document_job(self, db):
        doc = _make_doc(db, status="completed")
        job = _make_job(db, "index_document")
        worker = JobWorker()
        worker._dispatch(db, job)
        refreshed = DocumentRepo(db).get(doc.id)
        assert refreshed.semantic_status == "indexed"
