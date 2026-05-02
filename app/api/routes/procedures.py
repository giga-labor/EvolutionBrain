from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.procedures import ProcedureRepo
from app.audit.service import AuditService
from app.schemas.procedures import ProcedureCreate, ProcedureRead, ProcedureUpdate
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def list_procedures(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    items = ProcedureRepo(db).list(limit=limit, offset=offset)
    reads = [ProcedureRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_procedure(payload: ProcedureCreate, db: Session = Depends(get_db)):
    item = ProcedureRepo(db).create(**payload.model_dump())
    AuditService(db).log("procedure", item.id, "create")
    return common.ok(ProcedureRead.model_validate(item).model_dump(mode="json"))


@router.get("/{procedure_id}", response_model=common.ApiResponse)
def get_procedure(procedure_id: str, db: Session = Depends(get_db)):
    item = ProcedureRepo(db).get(procedure_id)
    if not item:
        return common.err("not_found", f"Procedure '{procedure_id}' not found")
    return common.ok(ProcedureRead.model_validate(item).model_dump(mode="json"))


@router.patch("/{procedure_id}", response_model=common.ApiResponse)
def update_procedure(procedure_id: str, payload: ProcedureUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    item = ProcedureRepo(db).update(procedure_id, **updates)
    if not item:
        return common.err("not_found", f"Procedure '{procedure_id}' not found")
    AuditService(db).log("procedure", item.id, "update", updates)
    return common.ok(ProcedureRead.model_validate(item).model_dump(mode="json"))


@router.delete("/{procedure_id}", response_model=common.ApiResponse)
def delete_procedure(procedure_id: str, db: Session = Depends(get_db)):
    deleted = ProcedureRepo(db).delete(procedure_id)
    if not deleted:
        return common.err("not_found", f"Procedure '{procedure_id}' not found")
    AuditService(db).log("procedure", procedure_id, "delete")
    return common.ok({"deleted": True, "id": procedure_id})
