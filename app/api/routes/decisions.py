from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.decisions import DecisionRepo
from app.audit.service import AuditService
from app.schemas.decisions import DecisionCreate, DecisionRead, DecisionUpdate
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def list_decisions(
    limit: int = 100,
    offset: int = 0,
    project_id: str | None = None,
    db: Session = Depends(get_db),
):
    items = DecisionRepo(db).list(limit=limit, offset=offset, project_id=project_id)
    reads = [DecisionRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_decision(payload: DecisionCreate, db: Session = Depends(get_db)):
    item = DecisionRepo(db).create(**payload.model_dump())
    AuditService(db).log("decision", item.id, "create")
    return common.ok(DecisionRead.model_validate(item).model_dump(mode="json"))


@router.get("/{decision_id}", response_model=common.ApiResponse)
def get_decision(decision_id: str, db: Session = Depends(get_db)):
    item = DecisionRepo(db).get(decision_id)
    if not item:
        return common.err("not_found", f"Decision '{decision_id}' not found")
    return common.ok(DecisionRead.model_validate(item).model_dump(mode="json"))


@router.patch("/{decision_id}", response_model=common.ApiResponse)
def update_decision(decision_id: str, payload: DecisionUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    item = DecisionRepo(db).update(decision_id, **updates)
    if not item:
        return common.err("not_found", f"Decision '{decision_id}' not found")
    AuditService(db).log("decision", item.id, "update", updates)
    return common.ok(DecisionRead.model_validate(item).model_dump(mode="json"))


@router.delete("/{decision_id}", response_model=common.ApiResponse)
def delete_decision(decision_id: str, db: Session = Depends(get_db)):
    deleted = DecisionRepo(db).delete(decision_id)
    if not deleted:
        return common.err("not_found", f"Decision '{decision_id}' not found")
    AuditService(db).log("decision", decision_id, "delete")
    return common.ok({"deleted": True, "id": decision_id})
