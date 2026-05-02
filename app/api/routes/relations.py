from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.relations import RelationRepo
from app.audit.service import AuditService
from app.schemas.relations import RelationCreate, RelationRead, RelationUpdate
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def list_relations(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    items = RelationRepo(db).list(limit=limit, offset=offset)
    reads = [RelationRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_relation(payload: RelationCreate, db: Session = Depends(get_db)):
    item = RelationRepo(db).create(**payload.model_dump())
    AuditService(db).log("relation", item.id, "create")
    return common.ok(RelationRead.model_validate(item).model_dump(mode="json"))


@router.get("/{relation_id}", response_model=common.ApiResponse)
def get_relation(relation_id: str, db: Session = Depends(get_db)):
    item = RelationRepo(db).get(relation_id)
    if not item:
        return common.err("not_found", f"Relation '{relation_id}' not found")
    return common.ok(RelationRead.model_validate(item).model_dump(mode="json"))


@router.patch("/{relation_id}", response_model=common.ApiResponse)
def update_relation(relation_id: str, payload: RelationUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    item = RelationRepo(db).update(relation_id, **updates)
    if not item:
        return common.err("not_found", f"Relation '{relation_id}' not found")
    AuditService(db).log("relation", item.id, "update", updates)
    return common.ok(RelationRead.model_validate(item).model_dump(mode="json"))


@router.delete("/{relation_id}", response_model=common.ApiResponse)
def delete_relation(relation_id: str, db: Session = Depends(get_db)):
    deleted = RelationRepo(db).delete(relation_id)
    if not deleted:
        return common.err("not_found", f"Relation '{relation_id}' not found")
    AuditService(db).log("relation", relation_id, "delete")
    return common.ok({"deleted": True, "id": relation_id})
