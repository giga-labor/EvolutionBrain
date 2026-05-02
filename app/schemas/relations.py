from datetime import datetime
from pydantic import BaseModel, Field


class RelationCreate(BaseModel):
    source_id: str = Field(min_length=1)
    target_id: str = Field(min_length=1)
    relation_type: str = Field(min_length=1)
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)
    evidence: str | None = None


class RelationUpdate(BaseModel):
    relation_type: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    evidence: str | None = None


class RelationRead(BaseModel):
    id: str
    source_id: str
    target_id: str
    relation_type: str
    confidence: float
    evidence: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
