from app.audit.service import AuditService
from app.db.repositories.notes import NoteRepo
from app.db.repositories.documents import DocumentRepo
from app.db.repositories.concepts import ConceptRepo
from app.db.repositories.tasks import TaskRepo
from app.db.repositories.goals import GoalRepo
from app.db.repositories.relations import RelationRepo

_RISK_MAP = {
    "create_note": "low",
    "update_note": "low",
    "create_task": "low",
    "update_task": "low",
    "create_concept": "low",
    "update_concept": "medium",
    "create_relation": "medium",
    "update_relation": "medium",
    "delete_note": "high",
    "delete_document": "high",
    "delete_concept": "high",
    "delete_task": "high",
    "bulk_update": "high",
    "merge_concepts": "critical",
    "reset_memory": "critical",
}

_CONFIRM_REQUIRED = {
    "delete_note", "delete_document", "delete_concept",
    "delete_task", "bulk_update", "merge_concepts", "reset_memory",
}


class ActionService:
    def __init__(self, db=None):
        self.db = db

    def plan(self, action_request: dict) -> dict:
        action_type = action_request.get("type", "unknown")
        risk = _RISK_MAP.get(action_type, "medium")
        requires_confirmation = action_type in _CONFIRM_REQUIRED
        return {
            "status": "ok",
            "action_type": action_type,
            "risk": risk,
            "requires_confirmation": requires_confirmation,
            "estimated_impact": risk,
            "action_request": action_request,
        }

    def execute(self, action_request: dict) -> dict:
        plan = self.plan(action_request)

        if action_request.get("dry_run", False):
            return {"status": "ok", "executed": False, "dry_run": True, "plan": plan}

        if plan["requires_confirmation"] and not action_request.get("confirmed", False):
            return {
                "status": "blocked",
                "executed": False,
                "reason": "confirmation_required",
                "plan": plan,
            }

        if self.db is None:
            return {"status": "error", "executed": False, "reason": "no_db_session"}

        return self._dispatch(action_request, plan)

    def _dispatch(self, req: dict, plan: dict) -> dict:
        action_type = req.get("type", "unknown")
        target_id = req.get("target_id")
        payload = req.get("payload") or {}
        actor = req.get("actor", "user")
        audit = AuditService(self.db)
        result_id = None

        try:
            if action_type == "create_note":
                item = NoteRepo(self.db).create(**payload)
                result_id = item.id
                audit.log("note", item.id, "action.create_note", payload, actor)

            elif action_type == "update_note":
                item = NoteRepo(self.db).update(target_id, **payload)
                result_id = target_id
                audit.log("note", target_id, "action.update_note", payload, actor)

            elif action_type == "delete_note":
                NoteRepo(self.db).delete(target_id)
                result_id = target_id
                audit.log("note", target_id, "action.delete_note", {}, actor)

            elif action_type == "create_task":
                item = TaskRepo(self.db).create(**payload)
                result_id = item.id
                audit.log("task", item.id, "action.create_task", payload, actor)

            elif action_type == "update_task":
                item = TaskRepo(self.db).update(target_id, **payload)
                result_id = target_id
                audit.log("task", target_id, "action.update_task", payload, actor)

            elif action_type == "delete_task":
                TaskRepo(self.db).delete(target_id)
                result_id = target_id
                audit.log("task", target_id, "action.delete_task", {}, actor)

            elif action_type == "create_concept":
                item = ConceptRepo(self.db).create(**payload)
                result_id = item.id
                audit.log("concept", item.id, "action.create_concept", payload, actor)

            elif action_type == "update_concept":
                item = ConceptRepo(self.db).update(target_id, **payload)
                result_id = target_id
                audit.log("concept", target_id, "action.update_concept", payload, actor)

            elif action_type == "delete_concept":
                ConceptRepo(self.db).delete(target_id)
                result_id = target_id
                audit.log("concept", target_id, "action.delete_concept", {}, actor)

            elif action_type == "delete_document":
                DocumentRepo(self.db).delete(target_id)
                result_id = target_id
                audit.log("document", target_id, "action.delete_document", {}, actor)

            elif action_type == "create_relation":
                item = RelationRepo(self.db).create(**payload)
                result_id = item.id
                audit.log("relation", item.id, "action.create_relation", payload, actor)

            else:
                return {
                    "status": "error",
                    "executed": False,
                    "reason": f"unknown action_type: {action_type}",
                    "plan": plan,
                }

        except Exception as exc:
            return {
                "status": "error",
                "executed": False,
                "reason": str(exc),
                "plan": plan,
            }

        return {
            "status": "ok",
            "executed": True,
            "action_type": action_type,
            "result_id": result_id,
            "risk": plan["risk"],
        }
