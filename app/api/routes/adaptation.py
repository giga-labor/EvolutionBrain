from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.adaptation.service import AdaptationService
from app.schemas import common

router = APIRouter()


@router.post("/feedback", response_model=common.ApiResponse)
def apply_feedback(feedback: dict, db: Session = Depends(get_db)):
    result = AdaptationService(db).apply_feedback(feedback)
    return common.ok(result)
