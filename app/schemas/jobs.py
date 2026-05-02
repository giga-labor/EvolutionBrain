from datetime import datetime
from pydantic import BaseModel


class JobCreate(BaseModel):
    job_type: str
    priority: float = 0.0


class JobRead(BaseModel):
    id: str
    job_type: str
    status: str
    priority: float
    retry_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
