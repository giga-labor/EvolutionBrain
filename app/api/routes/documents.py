import hashlib
from uuid import uuid4
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.documents import DocumentRepo
from app.audit.service import AuditService
from app.ingestion.service import IngestionService
from app.schemas.documents import DocumentCreate, DocumentImport, DocumentUpdate, DocumentRead
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def list_documents(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    items = DocumentRepo(db).list(limit=limit, offset=offset)
    reads = [DocumentRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("/import", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def import_document(payload: DocumentImport, db: Session = Depends(get_db)):
    result = IngestionService(db).import_text(
        content=payload.content,
        title=payload.title,
        source_type=payload.source_type,
        source_ref=payload.source_ref,
    )
    return common.ok(result)


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    repo = DocumentRepo(db)
    content_hash = hashlib.sha256(str(uuid4()).encode("utf-8")).hexdigest()
    doc = repo.create(
        source_type=payload.source_type,
        source_ref=payload.source_ref,
        title=payload.title,
        content_hash=content_hash,
        raw_content=None,
        ingestion_status="raw_pending",
        normalization_status="pending",
        semantic_status="pending",
        validation_status="unvalidated",
    )
    AuditService(db).log("document", doc.id, "create")
    return common.ok(DocumentRead.model_validate(doc).model_dump(mode="json"))


@router.get("/{document_id}", response_model=common.ApiResponse)
def get_document(document_id: str, db: Session = Depends(get_db)):
    doc = DocumentRepo(db).get(document_id)
    if not doc:
        return common.err("not_found", f"Document '{document_id}' not found")
    return common.ok(DocumentRead.model_validate(doc).model_dump(mode="json"))


@router.patch("/{document_id}", response_model=common.ApiResponse)
def update_document(document_id: str, payload: DocumentUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    doc = DocumentRepo(db).update(document_id, **updates)
    if not doc:
        return common.err("not_found", f"Document '{document_id}' not found")
    AuditService(db).log("document", doc.id, "update", updates)
    return common.ok(DocumentRead.model_validate(doc).model_dump(mode="json"))


@router.delete("/{document_id}", response_model=common.ApiResponse)
def delete_document(document_id: str, db: Session = Depends(get_db)):
    deleted = DocumentRepo(db).delete(document_id)
    if not deleted:
        return common.err("not_found", f"Document '{document_id}' not found")
    AuditService(db).log("document", document_id, "delete")
    return common.ok({"deleted": True, "id": document_id})
