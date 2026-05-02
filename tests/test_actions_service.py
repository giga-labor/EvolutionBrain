import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.repositories.notes import NoteRepo
from app.db.repositories.tasks import TaskRepo
from app.db.repositories.concepts import ConceptRepo
from app.actions.service import ActionService


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


class TestActionPlan:
    def test_plan_delete_is_high_risk(self):
        svc = ActionService()
        plan = svc.plan({"type": "delete_note"})
        assert plan["risk"] == "high"
        assert plan["requires_confirmation"] is True

    def test_plan_create_is_low_risk(self):
        svc = ActionService()
        plan = svc.plan({"type": "create_note"})
        assert plan["risk"] == "low"
        assert plan["requires_confirmation"] is False

    def test_plan_merge_is_critical(self):
        svc = ActionService()
        plan = svc.plan({"type": "merge_concepts"})
        assert plan["risk"] == "critical"


class TestActionExecute:
    def test_dry_run_does_not_mutate(self, db):
        svc = ActionService(db)
        result = svc.execute({
            "type": "create_note",
            "payload": {"title": "dry", "body_markdown": "x", "note_type": "g", "source_type": "manual"},
            "dry_run": True,
        })
        assert result["executed"] is False
        assert result["dry_run"] is True
        assert NoteRepo(db).list() == []

    def test_delete_requires_confirmation(self, db):
        note = NoteRepo(db).create(
            title="to-delete", body_markdown="x", note_type="g", source_type="manual"
        )
        svc = ActionService(db)
        result = svc.execute({"type": "delete_note", "target_id": note.id})
        assert result["status"] == "blocked"
        assert result["executed"] is False
        assert NoteRepo(db).get(note.id) is not None

    def test_delete_with_confirmation_removes_note(self, db):
        note = NoteRepo(db).create(
            title="to-delete", body_markdown="x", note_type="g", source_type="manual"
        )
        svc = ActionService(db)
        result = svc.execute({
            "type": "delete_note",
            "target_id": note.id,
            "confirmed": True,
        })
        assert result["executed"] is True
        assert NoteRepo(db).get(note.id) is None

    def test_create_note_persists(self, db):
        svc = ActionService(db)
        result = svc.execute({
            "type": "create_note",
            "payload": {"title": "New Note", "body_markdown": "body", "note_type": "generic", "source_type": "manual"},
        })
        assert result["executed"] is True
        assert result["result_id"] is not None
        note = NoteRepo(db).get(result["result_id"])
        assert note is not None
        assert note.title == "New Note"

    def test_create_task_persists(self, db):
        svc = ActionService(db)
        result = svc.execute({
            "type": "create_task",
            "payload": {"title": "My Task", "priority": 0.7},
        })
        assert result["executed"] is True
        task = TaskRepo(db).get(result["result_id"])
        assert task.title == "My Task"

    def test_unknown_action_returns_error(self, db):
        svc = ActionService(db)
        result = svc.execute({"type": "fly_to_moon"})
        assert result["status"] == "error"
        assert result["executed"] is False
