from datetime import datetime
from pydantic import BaseModel, Field


class SourceProfileCreate(BaseModel):
    name: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)


class SourceProfileRead(BaseModel):
    id: str
    name: str
    source_type: str
    source_ref: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SourceSyncUpdatesRequest(BaseModel):
    source_path: str | None = None
