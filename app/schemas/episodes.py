from datetime import datetime
from pydantic import BaseModel, Field


class EpisodeCreate(BaseModel):
    title: str = Field(min_length=1)
    context: str | None = None
    outcome: str | None = None
    confidence: float = Field(default=0.6, ge=0.0, le=1.0)


class EpisodeUpdate(BaseModel):
    title: str | None = None
    context: str | None = None
    outcome: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class EpisodeRead(BaseModel):
    id: str
    title: str
    context: str | None
    outcome: str | None
    confidence: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
