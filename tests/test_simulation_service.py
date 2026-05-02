import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.repositories.episodes import EpisodeRepo
from app.simulation.service import SimulationService


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


class TestSimulationService:
    def test_creates_episode_with_scenario_label(self, db):
        svc = SimulationService(db)
        result = svc.run_scenario({
            "title": "Test Scenario",
            "premise": "What if we do X?",
            "options": ["Option A", "Option B"],
        })
        assert result["status"] == "ok"
        assert result["epistemic_type"] == "scenario"
        assert result["scenario_id"] is not None
        episode = EpisodeRepo(db).get(result["scenario_id"])
        assert episode is not None
        assert "[SCENARIO]" in episode.title

    def test_options_ranked_by_confidence(self, db):
        svc = SimulationService(db)
        result = svc.run_scenario({
            "title": "Ranking Test",
            "premise": "some premise",
            "options": ["opt1", "opt2", "opt3"],
        })
        opts = result["evaluated_options"]
        confidences = [o["confidence"] for o in opts]
        assert confidences == sorted(confidences, reverse=True)

    def test_options_have_rank(self, db):
        svc = SimulationService(db)
        result = svc.run_scenario({
            "title": "Rank Test",
            "premise": "premise",
            "options": ["A", "B"],
        })
        for i, opt in enumerate(result["evaluated_options"]):
            assert opt["rank"] == i + 1

    def test_empty_options(self, db):
        svc = SimulationService(db)
        result = svc.run_scenario({"title": "Empty", "premise": "no opts", "options": []})
        assert result["status"] == "ok"
        assert result["evaluated_options"] == []

    def test_confidence_in_valid_range(self, db):
        svc = SimulationService(db)
        result = svc.run_scenario({
            "title": "Range Test",
            "premise": "premise",
            "options": ["x", "y", "z"],
        })
        for opt in result["evaluated_options"]:
            assert 0.0 <= opt["confidence"] <= 1.0

    def test_limitations_always_present(self, db):
        svc = SimulationService(db)
        result = svc.run_scenario({"title": "T", "premise": "p", "options": ["a"]})
        assert len(result["limitations"]) > 0
