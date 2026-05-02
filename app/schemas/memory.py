from datetime import datetime
from pydantic import BaseModel, Field


class MemoryItemCreate(BaseModel):
    object_type: str = Field(min_length=1)
    object_id: str = Field(min_length=1)
    layer: str = "active"
    relevance_score: float = 0.0
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)


class MemoryItemUpdate(BaseModel):
    layer: str | None = None
    relevance_score: float | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class MemoryItemRead(BaseModel):
    id: str
    object_type: str
    object_id: str
    layer: str
    relevance_score: float
    confidence: float
    access_count: int
    last_accessed_at: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
