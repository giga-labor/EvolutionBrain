from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.goals import GoalRepo
from app.audit.service import AuditService
from app.goals.service import GoalService
from app.schemas.goals import GoalCreate, GoalRead, GoalUpdate
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def list_goals(
    limit: int = 100,
    offset: int = 0,
    project_id: str | None = None,
    db: Session = Depends(get_db),
):
    items = GoalRepo(db).list(limit=limit, offset=offset, project_id=project_id)
    reads = [GoalRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_goal(payload: GoalCreate, db: Session = Depends(get_db)):
    item = GoalRepo(db).create(**payload.model_dump())
    AuditService(db).log("goal", item.id, "create")
    return common.ok(GoalRead.model_validate(item).model_dump(mode="json"))


@router.get("/{goal_id}", response_model=common.ApiResponse)
def get_goal(goal_id: str, db: Session = Depends(get_db)):
    item = GoalRepo(db).get(goal_id)
    if not item:
        return common.err("not_found", f"Goal '{goal_id}' not found")
    return common.ok(GoalRead.model_validate(item).model_dump(mode="json"))


@router.patch("/{goal_id}", response_model=common.ApiResponse)
def update_goal(goal_id: str, payload: GoalUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    item = GoalRepo(db).update(goal_id, **updates)
    if not item:
        return common.err("not_found", f"Goal '{goal_id}' not found")
    AuditService(db).log("goal", item.id, "update", updates)
    return common.ok(GoalRead.model_validate(item).model_dump(mode="json"))


@router.post("/recalculate", response_model=common.ApiResponse)
def recalculate_goals(db: Session = Depends(get_db)):
    result = GoalService(db).recalculate_priorities()
    AuditService(db).log("goal", "all", "recalculate", result)
    return common.ok(result)


@router.delete("/{goal_id}", response_model=common.ApiResponse)
def delete_goal(goal_id: str, db: Session = Depends(get_db)):
    deleted = GoalRepo(db).delete(goal_id)
    if not deleted:
        return common.err("not_found", f"Goal '{goal_id}' not found")
    AuditService(db).log("goal", goal_id, "delete")
    return common.ok({"deleted": True, "id": goal_id})
