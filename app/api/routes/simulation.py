from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.simulation.service import SimulationService
from app.schemas import common

router = APIRouter()


@router.post("/run", response_model=common.ApiResponse)
def run_simulation(scenario: dict, db: Session = Depends(get_db)):
    result = SimulationService(db).run_scenario(scenario)
    return common.ok(result)
