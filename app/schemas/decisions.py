from datetime import datetime
from pydantic import BaseModel, Field


class DecisionCreate(BaseModel):
    project_id: str | None = None
    title: str = Field(min_length=1)
    rationale: str | None = None


class DecisionUpdate(BaseModel):
    title: str | None = None
    rationale: str | None = None
    status: str | None = None


class DecisionRead(BaseModel):
    id: str
    project_id: str | None
    title: str
    rationale: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
