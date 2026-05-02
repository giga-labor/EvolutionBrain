from datetime import datetime
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    project_id: str | None = None
    goal_id: str | None = None
    title: str = Field(min_length=1)
    description: str | None = None
    priority: float = Field(default=0.5, ge=0.0, le=1.0)


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: float | None = Field(default=None, ge=0.0, le=1.0)
    status: str | None = None


class TaskRead(BaseModel):
    id: str
    project_id: str | None
    goal_id: str | None
    title: str
    description: str | None
    priority: float
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
