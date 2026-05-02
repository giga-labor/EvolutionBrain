from datetime import datetime
from pydantic import BaseModel, Field


class ProcedureCreate(BaseModel):
    title: str = Field(min_length=1)
    steps_markdown: str = Field(min_length=1)


class ProcedureUpdate(BaseModel):
    title: str | None = None
    steps_markdown: str | None = None
    status: str | None = None


class ProcedureRead(BaseModel):
    id: str
    title: str
    steps_markdown: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
