from fastapi import APIRouter
from app.metacognition.service import MetacognitionService
from app.schemas import common

router = APIRouter()


@router.post("/evaluate", response_model=common.ApiResponse)
def evaluate(payload: dict):
    result = MetacognitionService().evaluate_output(payload)
    return common.ok(result)
