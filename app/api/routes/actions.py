from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.actions.service import ActionService
from app.schemas import common

router = APIRouter()


@router.post("/plan", response_model=common.ApiResponse)
def plan_action(action_request: dict, db: Session = Depends(get_db)):
    result = ActionService(db).plan(action_request)
    return common.ok(result)


@router.post("/execute", response_model=common.ApiResponse)
def execute_action(action_request: dict, db: Session = Depends(get_db)):
    result = ActionService(db).execute(action_request)
    if result.get("status") == "error":
        return common.err("action_error", result.get("reason", "execution failed"))
    return common.ok(result)
