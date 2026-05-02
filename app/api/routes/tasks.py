from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.tasks import TaskRepo
from app.audit.service import AuditService
from app.schemas.tasks import TaskCreate, TaskRead, TaskUpdate
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def list_tasks(
    limit: int = 100,
    offset: int = 0,
    project_id: str | None = None,
    db: Session = Depends(get_db),
):
    items = TaskRepo(db).list(limit=limit, offset=offset, project_id=project_id)
    reads = [TaskRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    item = TaskRepo(db).create(**payload.model_dump())
    AuditService(db).log("task", item.id, "create")
    return common.ok(TaskRead.model_validate(item).model_dump(mode="json"))


@router.get("/{task_id}", response_model=common.ApiResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    item = TaskRepo(db).get(task_id)
    if not item:
        return common.err("not_found", f"Task '{task_id}' not found")
    return common.ok(TaskRead.model_validate(item).model_dump(mode="json"))


@router.patch("/{task_id}", response_model=common.ApiResponse)
def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    item = TaskRepo(db).update(task_id, **updates)
    if not item:
        return common.err("not_found", f"Task '{task_id}' not found")
    AuditService(db).log("task", item.id, "update", updates)
    return common.ok(TaskRead.model_validate(item).model_dump(mode="json"))


@router.delete("/{task_id}", response_model=common.ApiResponse)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    deleted = TaskRepo(db).delete(task_id)
    if not deleted:
        return common.err("not_found", f"Task '{task_id}' not found")
    AuditService(db).log("task", task_id, "delete")
    return common.ok({"deleted": True, "id": task_id})
