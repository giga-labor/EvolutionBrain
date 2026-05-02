from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.audit import AuditRepo
from app.schemas.audit import AuditEntryRead
from app.schemas import common

router = APIRouter()


@router.get("/logs", response_model=common.ApiResponse)
def list_audit_logs(
    entity_type: str | None = None,
    entity_id: str | None = None,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    items = AuditRepo(db).list(entity_type=entity_type, entity_id=entity_id, limit=limit)
    reads = [AuditEntryRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})
