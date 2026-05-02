from datetime import datetime, timezone

from app.db.repositories.goals import GoalRepo
from app.audit.service import AuditService


class GoalService:
    def __init__(self, db):
        self.db = db
        self.repo = GoalRepo(db)
        self.audit = AuditService(db)

    def recalculate_priorities(self, project_id: str | None = None) -> dict:
        goals = self.repo.list(limit=10000, offset=0, project_id=project_id)
        updated = 0
        now = datetime.now(timezone.utc)

        for goal in goals:
            old_priority = goal.priority

            if goal.status in ("completed", "cancelled"):
                new_priority = 0.0
            elif goal.status == "paused":
                new_priority = max(0.0, round(goal.priority - 0.05, 4))
            else:
                base = goal.priority
                urgency_boost = 0.0
                due_date = getattr(goal, "due_date", None)
                if due_date:
                    try:
                        due = datetime.fromisoformat(due_date)
                        if due.tzinfo is None:
                            due = due.replace(tzinfo=timezone.utc)
                        days_to_due = (due - now).total_seconds() / 86400
                        if days_to_due > 0:
                            urgency_boost = min(0.30, max(0.0, 1.0 - days_to_due / 30))
                        else:
                            urgency_boost = 0.30  # Overdue: max boost
                    except (ValueError, TypeError):
                        pass
                new_priority = min(1.0, round(base + urgency_boost, 4))

            if new_priority != old_priority:
                self.repo.update(goal.id, priority=new_priority)
                updated += 1

        self.audit.log(
            "goal", project_id or "all", "goals.priorities_recalculated",
            {"updated": updated, "total": len(goals), "project_id": project_id},
        )
        return {"status": "ok", "recalculated": True, "updated": updated, "total": len(goals)}
