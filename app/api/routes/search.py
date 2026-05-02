from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.retrieval.service import RetrievalService
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def search(q: str = "", mode: str = "hybrid", limit: int = 20, db: Session = Depends(get_db)):
    result = RetrievalService(db).search(query=q, mode=mode, limit=limit)
    return common.ok(result)
