from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.self_model import SelfModelRepo
from app.audit.service import AuditService
from app.schemas.self_model import SelfModelRead, SelfModelUpdate
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def get_self_model(db: Session = Depends(get_db)):
    item = SelfModelRepo(db).get_singleton()
    return common.ok(SelfModelRead.model_validate(item).model_dump(mode="json"))


@router.put("", response_model=common.ApiResponse)
def put_self_model(payload: SelfModelUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    item = SelfModelRepo(db).update_singleton(**updates)
    AuditService(db).log("self_model", item.id, "update", updates)
    return common.ok(SelfModelRead.model_validate(item).model_dump(mode="json"))
