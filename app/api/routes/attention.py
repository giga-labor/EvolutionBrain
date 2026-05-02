from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.attention.service import AttentionService
from app.schemas import common

router = APIRouter()


@router.post("/focus", response_model=common.ApiResponse)
def pick_focus(payload: dict, db: Session = Depends(get_db)):
    candidates = payload.get("candidates", [])
    result = AttentionService().pick_focus(candidates, db=db)
    return common.ok(result)
