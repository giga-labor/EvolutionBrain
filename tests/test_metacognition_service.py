import pytest
from app.metacognition.service import MetacognitionService


@pytest.fixture
def svc():
    return MetacognitionService()


class TestMetacognitionService:
    def test_no_sources_warns_and_lowers_quality(self, svc):
        result = svc.evaluate_output({"answer": "test", "confidence": 0.5, "used_sources": []})
        assert result["context_sufficiency"] == "none"
        assert "no_sources_found" in result["warnings"]
        assert result["quality_score"] < 1.0

    def test_one_source_is_insufficient(self, svc):
        result = svc.evaluate_output({
            "answer": "test",
            "confidence": 0.5,
            "used_sources": [{"type": "note", "id": "a"}],
        })
        assert result["context_sufficiency"] == "insufficient"
        assert "low_source_count" in result["warnings"]

    def test_two_sources_is_sufficient(self, svc):
        result = svc.evaluate_output({
            "answer": "ok",
            "confidence": 0.5,
            "used_sources": [{"type": "note", "id": "a"}, {"type": "document", "id": "b"}],
        })
        assert result["context_sufficiency"] == "sufficient"
        assert "low_source_count" not in result["warnings"]

    def test_high_confidence_few_sources_flags_overconfidence(self, svc):
        result = svc.evaluate_output({
            "answer": "x",
            "confidence": 0.9,
            "used_sources": [{"type": "note", "id": "a"}],
        })
        assert result["overconfidence_risk"] == "high"
        assert "overconfidence_low_evidence" in result["warnings"]

    def test_diverse_source_types_boost_quality(self, svc):
        result = svc.evaluate_output({
            "answer": "test",
            "confidence": 0.5,
            "used_sources": [
                {"type": "note", "id": "a"},
                {"type": "document", "id": "b"},
                {"type": "concept", "id": "c"},
            ],
        })
        assert result["source_diversity"] >= 2
        assert result["quality_score"] >= 0.9

    def test_verbose_answer_few_sources_warns(self, svc):
        long_answer = "x" * 600
        result = svc.evaluate_output({
            "answer": long_answer,
            "confidence": 0.5,
            "used_sources": [{"type": "note", "id": "a"}],
        })
        assert "verbose_answer_low_evidence" in result["warnings"]

    def test_quality_score_clamped(self, svc):
        result = svc.evaluate_output({"answer": "", "confidence": 1.0, "used_sources": []})
        assert 0.0 <= result["quality_score"] <= 1.0

    def test_good_output_has_low_overconfidence(self, svc):
        result = svc.evaluate_output({
            "answer": "well-grounded",
            "confidence": 0.6,
            "used_sources": [{"type": "note", "id": "a"}, {"type": "document", "id": "b"}],
        })
        assert result["overconfidence_risk"] == "low"
