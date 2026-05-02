from app.audit.service import AuditService
from app.db.repositories.episodes import EpisodeRepo
from app.retrieval.service import RetrievalService


class SimulationService:
    def __init__(self, db):
        self.db = db
        self.audit = AuditService(db)

    def run_scenario(self, scenario: dict) -> dict:
        title = scenario.get("title", "Unnamed Scenario")
        premise = scenario.get("premise", "")
        options = scenario.get("options", [])
        constraints = scenario.get("constraints") or []
        actor = scenario.get("actor", "user")

        # Persist scenario as an Episode with epistemic_type=scenario
        episode = EpisodeRepo(self.db).create(
            title=f"[SCENARIO] {title}",
            context=premise,
            outcome=None,
            confidence=0.0,
        )

        # Retrieve knowledge evidence relevant to premise
        retrieval = RetrievalService(self.db)
        search_result = retrieval.hybrid_search(premise, limit=5) if premise.strip() else {}
        evidence_items = search_result.get("results", [])
        evidence_texts = [
            item.get("snippet") or item.get("title") or ""
            for item in evidence_items
        ]

        evaluated_options = []
        for option in options:
            option_tokens = set(option.lower().split())

            # Score: token overlap with evidence
            evidence_overlap = 0.0
            if evidence_texts:
                overlaps = [
                    len(option_tokens & set(e.lower().split())) / max(len(option_tokens), 1)
                    for e in evidence_texts if e
                ]
                evidence_overlap = sum(overlaps) / len(evidence_texts)

            # Constraint penalty
            constraint_penalty = 0.0
            for constraint in constraints:
                c_tokens = set(constraint.lower().split())
                overlap = len(option_tokens & c_tokens) / max(len(option_tokens), 1)
                constraint_penalty += overlap * 0.10

            confidence = round(
                max(0.10, min(0.90, 0.40 + evidence_overlap * 0.40 - constraint_penalty)),
                3,
            )
            impact = (
                "high" if confidence > 0.65
                else "medium" if confidence > 0.40
                else "low"
            )
            evaluated_options.append({
                "option": option,
                "confidence": confidence,
                "estimated_impact": impact,
                "evidence_overlap": round(evidence_overlap, 3),
            })

        # Rank by confidence descending
        evaluated_options.sort(key=lambda x: x["confidence"], reverse=True)
        for i, opt in enumerate(evaluated_options):
            opt["rank"] = i + 1

        self.audit.log(
            "episode", episode.id, "simulation.run",
            {"scenario_title": title, "options_count": len(options), "evidence_used": len(evidence_texts)},
            actor,
        )

        return {
            "status": "ok",
            "epistemic_type": "scenario",
            "scenario_id": episode.id,
            "scenario_title": title,
            "evaluated_options": evaluated_options,
            "evidence_used": len(evidence_texts),
            "limitations": [
                "Scenario outputs are epistemic_type=scenario and are never automatically promoted to validated knowledge.",
            ],
        }
