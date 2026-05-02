from datetime import datetime
from pydantic import BaseModel, Field


class ConceptCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)


class ConceptUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class ConceptRead(BaseModel):
    id: str
    name: str
    description: str | None
    status: str
    confidence: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
