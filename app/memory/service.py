import math
from datetime import datetime, timezone

from app.db.repositories.memory_items import MemoryItemRepo
from app.audit.service import AuditService

# Layer promotion order (lower index = less consolidated)
_LAYER_ORDER = [
    "raw", "processed", "active", "contextual",
    "strategic", "historical", "latent", "archived",
    "episodic", "procedural", "temporary",
]

# Minimum requirements to reach a layer
_LAYER_GATES = {
    "contextual": {"min_confidence": 0.5, "min_access": 1},
    "strategic":  {"min_confidence": 0.7, "min_access": 3},
    "historical": {"min_confidence": 0.0, "min_access": 0},
    "latent":     {"min_confidence": 0.0, "min_access": 0},
    "archived":   {"min_confidence": 0.0, "min_access": 0},
}


class MemoryService:
    def __init__(self, db):
        self.db = db
        self.repo = MemoryItemRepo(db)
        self.audit = AuditService(db)

    @staticmethod
    def _score(access_count: int, confidence: float, last_accessed_at: str | None) -> float:
        age_days = 0.0
        if last_accessed_at:
            try:
                last = datetime.fromisoformat(last_accessed_at)
                if last.tzinfo is None:
                    last = last.replace(tzinfo=timezone.utc)
                delta = datetime.now(timezone.utc) - last
                age_days = max(0.0, delta.total_seconds() / 86400)
            except (ValueError, TypeError):
                age_days = 0.0

        decay = math.exp(-0.05 * age_days)
        access_weight = min(access_count * 0.08, 0.40)
        confidence_weight = confidence * 0.45
        raw = 0.15 + access_weight + confidence_weight
        return round(min(1.0, raw) * decay, 4)

    def recalculate(self, scope: str = "all") -> dict:
        layer_filter = None if scope == "all" else scope
        items = self.repo.list(limit=10000, offset=0, layer=layer_filter)
        updated = 0
        for item in items:
            score = self._score(item.access_count, item.confidence, item.last_accessed_at)
            if score != item.relevance_score:
                self.repo.update(item.id, relevance_score=score)
                updated += 1
        return {"scope": scope, "status": "ok", "updated": updated, "total": len(items)}

    def promote(self, item_id: str, target_layer: str, actor: str = "system") -> dict:
        item = self.repo.get(item_id)
        if not item:
            return {"ok": False, "error": "not_found"}

        gates = _LAYER_GATES.get(target_layer, {})
        if item.confidence < gates.get("min_confidence", 0.0):
            return {
                "ok": False,
                "error": f"confidence {item.confidence:.2f} below minimum "
                         f"{gates['min_confidence']} required for layer '{target_layer}'",
            }
        if item.access_count < gates.get("min_access", 0):
            return {
                "ok": False,
                "error": f"access_count {item.access_count} below minimum "
                         f"{gates['min_access']} required for layer '{target_layer}'",
            }

        old_layer = item.layer
        updated = self.repo.update(item_id, layer=target_layer)
        self.audit.log(
            "memory_item", item_id, "memory.promoted",
            {"from_layer": old_layer, "to_layer": target_layer},
            actor,
        )
        return {"ok": True, "id": item_id, "from_layer": old_layer, "to_layer": target_layer,
                "confidence": updated.confidence, "access_count": updated.access_count}

    def demote(self, item_id: str, target_layer: str, actor: str = "system") -> dict:
        item = self.repo.get(item_id)
        if not item:
            return {"ok": False, "error": "not_found"}

        old_layer = item.layer
        updated = self.repo.update(item_id, layer=target_layer)
        self.audit.log(
            "memory_item", item_id, "memory.demoted",
            {"from_layer": old_layer, "to_layer": target_layer},
            actor,
        )
        return {"ok": True, "id": item_id, "from_layer": old_layer, "to_layer": target_layer}

    def auto_promote_demote(self, actor: str = "system") -> dict:
        items = self.repo.list(limit=10000)
        promoted = []
        demoted = []
        now = datetime.now(timezone.utc)

        for item in items:
            score = self._score(item.access_count, item.confidence, item.last_accessed_at)
            # Recalculate score first
            if score != item.relevance_score:
                self.repo.update(item.id, relevance_score=score)

            # Promote: high score + enough confidence + enough accesses + not already strategic
            if (
                score > 0.75
                and item.confidence >= 0.7
                and item.access_count >= 3
                and item.layer not in ("strategic", "historical", "archived", "latent")
            ):
                target = "contextual" if item.layer in ("raw", "processed", "active") else "strategic"
                result = self.promote(item.id, target, actor)
                if result.get("ok"):
                    promoted.append({"id": item.id, "to_layer": target, "score": score})
                continue

            # Demote: very low score + not accessed in >30 days
            days_since = 999
            if item.last_accessed_at:
                try:
                    last = datetime.fromisoformat(item.last_accessed_at)
                    if last.tzinfo is None:
                        last = last.replace(tzinfo=timezone.utc)
                    days_since = (now - last).total_seconds() / 86400
                except (ValueError, TypeError):
                    pass

            if (
                score < 0.25
                and days_since > 30
                and item.layer not in ("historical", "latent", "archived", "temporary")
            ):
                result = self.demote(item.id, "historical", actor)
                if result.get("ok"):
                    demoted.append({"id": item.id, "to_layer": "historical", "score": score})

        return {
            "ok": True,
            "promoted": promoted,
            "demoted": demoted,
            "promoted_count": len(promoted),
            "demoted_count": len(demoted),
        }
