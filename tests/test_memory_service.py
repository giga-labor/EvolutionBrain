import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.repositories.memory_items import MemoryItemRepo
from app.memory.service import MemoryService


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()


def _make_item(db, access_count=0, confidence=0.7, layer="active", last_accessed_at=None):
    return MemoryItemRepo(db).create(
        object_type="note",
        object_id="test-obj",
        layer=layer,
        relevance_score=0.0,
        confidence=confidence,
        access_count=access_count,
        last_accessed_at=last_accessed_at,
    )


class TestMemoryScoring:
    def test_score_zero_accesses_no_decay(self):
        score = MemoryService._score(0, 0.7, None)
        expected = round((0.15 + 0 + 0.7 * 0.45), 4)
        assert score == expected

    def test_score_decreases_with_age(self):
        import math
        score_fresh = MemoryService._score(5, 0.8, None)
        # Simulate 60 days old
        from datetime import datetime, timezone, timedelta
        old_date = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
        score_old = MemoryService._score(5, 0.8, old_date)
        assert score_old < score_fresh

    def test_score_capped_at_1(self):
        score = MemoryService._score(100, 1.0, None)
        assert score <= 1.0

    def test_recalculate_updates_items(self, db):
        item = _make_item(db, access_count=5, confidence=0.9)
        svc = MemoryService(db)
        result = svc.recalculate()
        assert result["status"] == "ok"
        assert result["total"] >= 1
        refreshed = MemoryItemRepo(db).get(item.id)
        # Score should not be 0 anymore
        assert refreshed.relevance_score > 0


class TestMemoryPromote:
    def test_promote_active_to_contextual(self, db):
        item = _make_item(db, access_count=2, confidence=0.6, layer="active")
        svc = MemoryService(db)
        result = svc.promote(item.id, "contextual")
        assert result["ok"] is True
        assert result["to_layer"] == "contextual"
        assert MemoryItemRepo(db).get(item.id).layer == "contextual"

    def test_promote_to_strategic_requires_confidence(self, db):
        item = _make_item(db, access_count=5, confidence=0.4, layer="active")
        svc = MemoryService(db)
        result = svc.promote(item.id, "strategic")
        assert result["ok"] is False
        assert "confidence" in result["error"]

    def test_promote_to_strategic_requires_accesses(self, db):
        item = _make_item(db, access_count=1, confidence=0.9, layer="active")
        svc = MemoryService(db)
        result = svc.promote(item.id, "strategic")
        assert result["ok"] is False
        assert "access_count" in result["error"]

    def test_promote_to_strategic_succeeds(self, db):
        item = _make_item(db, access_count=5, confidence=0.8, layer="active")
        svc = MemoryService(db)
        result = svc.promote(item.id, "strategic")
        assert result["ok"] is True
        assert MemoryItemRepo(db).get(item.id).layer == "strategic"

    def test_promote_not_found(self, db):
        svc = MemoryService(db)
        result = svc.promote("nonexistent-id", "active")
        assert result["ok"] is False
        assert result["error"] == "not_found"


class TestMemoryDemote:
    def test_demote_to_historical(self, db):
        item = _make_item(db, layer="strategic")
        svc = MemoryService(db)
        result = svc.demote(item.id, "historical")
        assert result["ok"] is True
        assert MemoryItemRepo(db).get(item.id).layer == "historical"

    def test_demote_not_found(self, db):
        svc = MemoryService(db)
        result = svc.demote("nonexistent-id", "historical")
        assert result["ok"] is False


class TestAutoPromoteDemote:
    def test_auto_promotes_high_score_item(self, db):
        from datetime import datetime, timezone
        recent = datetime.now(timezone.utc).isoformat()
        item = _make_item(db, access_count=10, confidence=0.9, layer="active", last_accessed_at=recent)
        svc = MemoryService(db)
        result = svc.auto_promote_demote()
        assert result["ok"] is True
        # Should have promoted this item
        assert result["promoted_count"] >= 1

    def test_auto_demotes_old_low_score_item(self, db):
        from datetime import datetime, timezone, timedelta
        old = (datetime.now(timezone.utc) - timedelta(days=45)).isoformat()
        item = _make_item(db, access_count=0, confidence=0.1, layer="active", last_accessed_at=old)
        svc = MemoryService(db)
        result = svc.auto_promote_demote()
        assert result["ok"] is True
        assert result["demoted_count"] >= 1
