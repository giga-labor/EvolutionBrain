from app.audit.service import AuditService
from app.db.repositories.memory_items import MemoryItemRepo
from app.db.repositories.notes import NoteRepo
from app.db.repositories.concepts import ConceptRepo


class AdaptationService:
    def __init__(self, db):
        self.db = db
        self.audit = AuditService(db)

    def apply_feedback(self, feedback: dict) -> dict:
        entity_type = feedback.get("entity_type", "")
        entity_id = feedback.get("entity_id", "")
        rating = feedback.get("rating")
        comment = feedback.get("comment")
        actor = feedback.get("actor", "user")

        score_delta = 0.0
        impact = "minimal"

        if isinstance(rating, (int, float)):
            # Scale rating 1–5 → delta [-0.2, +0.2]
            score_delta = max(-0.2, min(0.2, (float(rating) - 3.0) / 10.0))
            impact = (
                "significant" if abs(score_delta) >= 0.15
                else "moderate" if abs(score_delta) >= 0.05
                else "minimal"
            )

            if entity_type and entity_id:
                self._propagate_to_entity(entity_type, entity_id, score_delta)

            # Touch MemoryItem if linked
            if entity_type and entity_id:
                mem = MemoryItemRepo(self.db).get_by_object(entity_type, entity_id)
                if mem:
                    MemoryItemRepo(self.db).touch(mem.id)

            self.audit.log(
                entity_type or "unknown",
                entity_id or "unknown",
                "feedback.applied",
                {"rating": rating, "score_delta": round(score_delta, 4), "comment": comment},
                actor,
            )

        return {
            "status": "ok",
            "impact": impact,
            "score_delta": round(score_delta, 4),
            "entity_type": entity_type,
            "entity_id": entity_id,
            "feedback": feedback,
        }

    def _propagate_to_entity(self, entity_type: str, entity_id: str, delta: float):
        if entity_type == "note":
            note = NoteRepo(self.db).get(entity_id)
            if note:
                new_conf = round(max(0.0, min(1.0, note.confidence + delta)), 4)
                NoteRepo(self.db).update(entity_id, confidence=new_conf)

        elif entity_type == "concept":
            concept = ConceptRepo(self.db).get(entity_id)
            if concept:
                new_conf = round(max(0.0, min(1.0, concept.confidence + delta)), 4)
                ConceptRepo(self.db).update(entity_id, confidence=new_conf)

        elif entity_type == "memory_item":
            item = MemoryItemRepo(self.db).get(entity_id)
            if item:
                new_conf = round(max(0.0, min(1.0, item.confidence + delta)), 4)
                MemoryItemRepo(self.db).update(entity_id, confidence=new_conf)
