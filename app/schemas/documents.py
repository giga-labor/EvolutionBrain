from datetime import datetime
from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    source_type: str = "manual"
    source_ref: str | None = None
    title: str | None = None


class DocumentImport(BaseModel):
    content: str = Field(min_length=1)
    title: str | None = None
    source_type: str = "text"
    source_ref: str | None = None


class DocumentUpdate(BaseModel):
    title: str | None = None
    validation_status: str | None = None
    source_ref: str | None = None


class DocumentRead(BaseModel):
    id: str
    source_type: str
    source_ref: str | None
    title: str | None
    content_hash: str
    raw_content: str | None
    ingestion_status: str
    normalization_status: str
    semantic_status: str
    validation_status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
