from datetime import datetime, timezone


class AttentionService:
    def pick_focus(self, candidates: list[dict], db=None) -> dict:
        if not candidates:
            return {"focus": None, "reason": "no_candidates", "candidate_count": 0}

        now = datetime.now(timezone.utc)
        scored = []

        for c in candidates:
            composite = c.get("score", 0.0) * 0.50

            if db:
                try:
                    from app.db.repositories.memory_items import MemoryItemRepo
                    mem = MemoryItemRepo(db).get_by_object(
                        c.get("type", ""), c.get("id", "")
                    )
                    if mem:
                        # Recency bonus: items accessed within last 14 days score higher
                        if mem.last_accessed_at:
                            try:
                                last = datetime.fromisoformat(mem.last_accessed_at)
                                if last.tzinfo is None:
                                    last = last.replace(tzinfo=timezone.utc)
                                days_since = (now - last).total_seconds() / 86400
                                recency = max(0.0, 1.0 - days_since / 14)
                                composite += recency * 0.30
                            except (ValueError, TypeError):
                                pass

                        layer_bonus = {
                            "active": 0.15,
                            "contextual": 0.12,
                            "strategic": 0.10,
                        }.get(mem.layer, 0.0)
                        composite += layer_bonus
                except Exception:
                    pass

            scored.append((composite, c))

        best_score, best_candidate = max(scored, key=lambda x: x[0])
        return {
            "focus": best_candidate,
            "composite_score": round(best_score, 4),
            "reason": "highest_composite",
            "candidate_count": len(candidates),
        }
