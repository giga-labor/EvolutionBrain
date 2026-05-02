from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.sources import SourceProfileRepo
from app.audit.service import AuditService
from app.schemas.sources import SourceProfileCreate, SourceProfileRead, SourceSyncUpdatesRequest
from app.ingestion.incremental_service import IncrementalIngestionService
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def list_sources(limit: int = 200, offset: int = 0, source_type: str | None = None, db: Session = Depends(get_db)):
    items = SourceProfileRepo(db).list(limit=limit, offset=offset, source_type=source_type)
    reads = [SourceProfileRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_source(payload: SourceProfileCreate, db: Session = Depends(get_db)):
    item = SourceProfileRepo(db).create(**payload.model_dump())
    AuditService(db).log("source_profile", item.id, "create")
    return common.ok(SourceProfileRead.model_validate(item).model_dump(mode="json"))


@router.delete("/{source_id}", response_model=common.ApiResponse)
def delete_source(source_id: str, db: Session = Depends(get_db)):
    deleted = SourceProfileRepo(db).delete(source_id)
    if not deleted:
        return common.err("not_found", f"Source profile '{source_id}' not found")
    AuditService(db).log("source_profile", source_id, "delete")
    return common.ok({"deleted": True, "id": source_id})


@router.post("/{source_id}/sync-updates", response_model=common.ApiResponse)
def sync_source_updates(source_id: str, payload: SourceSyncUpdatesRequest, db: Session = Depends(get_db)):
    source = SourceProfileRepo(db).get(source_id)
    if not source:
        return common.err("not_found", f"Source profile '{source_id}' not found")
    source_path = payload.source_path or source.source_ref
    result = IncrementalIngestionService(db).sync_source_updates(
        source_profile_id=source_id,
        source_path=source_path,
    )
    if not result.get("ok"):
        return common.err("sync_failed", result.get("error", "sync failed"))
    return common.ok(result)
