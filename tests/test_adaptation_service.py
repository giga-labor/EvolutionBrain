import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.repositories.notes import NoteRepo
from app.db.repositories.concepts import ConceptRepo
from app.adaptation.service import AdaptationService


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


def _make_note(db, confidence=0.5):
    return NoteRepo(db).create(
        title="Test Note",
        body_markdown="body",
        note_type="generic",
        source_type="manual",
        confidence=confidence,
    )


def _make_concept(db, confidence=0.5):
    return ConceptRepo(db).create(name="TestConcept", confidence=confidence)


class TestAdaptationService:
    def test_positive_rating_increases_confidence(self, db):
        note = _make_note(db, confidence=0.5)
        svc = AdaptationService(db)
        result = svc.apply_feedback({
            "entity_type": "note",
            "entity_id": note.id,
            "rating": 5,
        })
        assert result["status"] == "ok"
        assert result["score_delta"] > 0
        updated = NoteRepo(db).get(note.id)
        assert updated.confidence > 0.5

    def test_negative_rating_decreases_confidence(self, db):
        note = _make_note(db, confidence=0.5)
        svc = AdaptationService(db)
        result = svc.apply_feedback({
            "entity_type": "note",
            "entity_id": note.id,
            "rating": 1,
        })
        assert result["score_delta"] < 0
        updated = NoteRepo(db).get(note.id)
        assert updated.confidence < 0.5

    def test_neutral_rating_minimal_delta(self, db):
        note = _make_note(db, confidence=0.5)
        svc = AdaptationService(db)
        result = svc.apply_feedback({
            "entity_type": "note",
            "entity_id": note.id,
            "rating": 3,
        })
        assert result["score_delta"] == 0.0
        assert result["impact"] == "minimal"

    def test_confidence_clamped_to_1(self, db):
        note = _make_note(db, confidence=0.95)
        svc = AdaptationService(db)
        svc.apply_feedback({"entity_type": "note", "entity_id": note.id, "rating": 5})
        updated = NoteRepo(db).get(note.id)
        assert updated.confidence <= 1.0

    def test_confidence_clamped_to_0(self, db):
        note = _make_note(db, confidence=0.05)
        svc = AdaptationService(db)
        svc.apply_feedback({"entity_type": "note", "entity_id": note.id, "rating": 1})
        updated = NoteRepo(db).get(note.id)
        assert updated.confidence >= 0.0

    def test_concept_confidence_updated(self, db):
        concept = _make_concept(db, confidence=0.5)
        svc = AdaptationService(db)
        svc.apply_feedback({"entity_type": "concept", "entity_id": concept.id, "rating": 5})
        updated = ConceptRepo(db).get(concept.id)
        assert updated.confidence > 0.5

    def test_nonexistent_entity_no_crash(self, db):
        svc = AdaptationService(db)
        result = svc.apply_feedback({
            "entity_type": "note",
            "entity_id": "nonexistent-id",
            "rating": 4,
        })
        assert result["status"] == "ok"

    def test_no_rating_zero_delta(self, db):
        svc = AdaptationService(db)
        result = svc.apply_feedback({"entity_type": "note", "entity_id": "x"})
        assert result["score_delta"] == 0.0
