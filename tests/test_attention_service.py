import pytest
from app.attention.service import AttentionService


class TestAttentionService:
    def test_empty_candidates_returns_no_focus(self):
        svc = AttentionService()
        result = svc.pick_focus([])
        assert result["focus"] is None
        assert result["reason"] == "no_candidates"
        assert result["candidate_count"] == 0

    def test_picks_highest_score(self):
        candidates = [
            {"type": "note", "id": "a", "score": 0.3, "title": "Low"},
            {"type": "note", "id": "b", "score": 0.9, "title": "High"},
            {"type": "note", "id": "c", "score": 0.5, "title": "Mid"},
        ]
        svc = AttentionService()
        result = svc.pick_focus(candidates)
        assert result["focus"]["id"] == "b"
        assert result["candidate_count"] == 3

    def test_composite_score_without_db(self):
        candidates = [{"type": "document", "id": "x", "score": 0.8}]
        svc = AttentionService()
        result = svc.pick_focus(candidates)
        assert result["composite_score"] == round(0.8 * 0.5, 4)

    def test_single_candidate_always_selected(self):
        candidates = [{"type": "concept", "id": "z", "score": 0.1}]
        svc = AttentionService()
        result = svc.pick_focus(candidates)
        assert result["focus"]["id"] == "z"
        assert result["reason"] == "highest_composite"

    def test_with_db_no_memory_item(self):
        """When db is provided but no MemoryItem exists, falls back to score only."""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.pool import StaticPool
        from app.db.base import Base

        engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        db = Session()

        candidates = [
            {"type": "note", "id": "no-mem-1", "score": 0.6},
            {"type": "note", "id": "no-mem-2", "score": 0.4},
        ]
        svc = AttentionService()
        result = svc.pick_focus(candidates, db=db)
        assert result["focus"]["id"] == "no-mem-1"

        db.close()
        Base.metadata.drop_all(engine)
        engine.dispose()
