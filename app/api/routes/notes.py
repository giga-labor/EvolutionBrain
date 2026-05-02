from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.notes import NoteRepo
from app.audit.service import AuditService
from app.schemas.notes import NoteCreate, NoteUpdate, NoteRead
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def list_notes(
    limit: int = 100,
    offset: int = 0,
    document_id: str | None = None,
    db: Session = Depends(get_db),
):
    items = NoteRepo(db).list(limit=limit, offset=offset, document_id=document_id)
    reads = [NoteRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    note = NoteRepo(db).create(**payload.model_dump())
    AuditService(db).log("note", note.id, "create")
    return common.ok(NoteRead.model_validate(note).model_dump(mode="json"))


@router.get("/{note_id}", response_model=common.ApiResponse)
def get_note(note_id: str, db: Session = Depends(get_db)):
    note = NoteRepo(db).get(note_id)
    if not note:
        return common.err("not_found", f"Note '{note_id}' not found")
    return common.ok(NoteRead.model_validate(note).model_dump(mode="json"))


@router.patch("/{note_id}", response_model=common.ApiResponse)
def update_note(note_id: str, payload: NoteUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    note = NoteRepo(db).update(note_id, **updates)
    if not note:
        return common.err("not_found", f"Note '{note_id}' not found")
    AuditService(db).log("note", note.id, "update", updates)
    return common.ok(NoteRead.model_validate(note).model_dump(mode="json"))


@router.delete("/{note_id}", response_model=common.ApiResponse)
def delete_note(note_id: str, db: Session = Depends(get_db)):
    deleted = NoteRepo(db).delete(note_id)
    if not deleted:
        return common.err("not_found", f"Note '{note_id}' not found")
    AuditService(db).log("note", note_id, "delete")
    return common.ok({"deleted": True, "id": note_id})
