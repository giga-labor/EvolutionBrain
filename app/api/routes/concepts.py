from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.concepts import ConceptRepo
from app.audit.service import AuditService
from app.schemas.concepts import ConceptCreate, ConceptRead, ConceptUpdate
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def list_concepts(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    items = ConceptRepo(db).list(limit=limit, offset=offset)
    reads = [ConceptRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_concept(payload: ConceptCreate, db: Session = Depends(get_db)):
    item = ConceptRepo(db).create(**payload.model_dump())
    AuditService(db).log("concept", item.id, "create")
    return common.ok(ConceptRead.model_validate(item).model_dump(mode="json"))


@router.get("/{concept_id}", response_model=common.ApiResponse)
def get_concept(concept_id: str, db: Session = Depends(get_db)):
    item = ConceptRepo(db).get(concept_id)
    if not item:
        return common.err("not_found", f"Concept '{concept_id}' not found")
    return common.ok(ConceptRead.model_validate(item).model_dump(mode="json"))


@router.patch("/{concept_id}", response_model=common.ApiResponse)
def update_concept(concept_id: str, payload: ConceptUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    item = ConceptRepo(db).update(concept_id, **updates)
    if not item:
        return common.err("not_found", f"Concept '{concept_id}' not found")
    AuditService(db).log("concept", item.id, "update", updates)
    return common.ok(ConceptRead.model_validate(item).model_dump(mode="json"))


@router.delete("/{concept_id}", response_model=common.ApiResponse)
def delete_concept(concept_id: str, db: Session = Depends(get_db)):
    deleted = ConceptRepo(db).delete(concept_id)
    if not deleted:
        return common.err("not_found", f"Concept '{concept_id}' not found")
    AuditService(db).log("concept", concept_id, "delete")
    return common.ok({"deleted": True, "id": concept_id})
