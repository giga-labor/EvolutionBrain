from datetime import datetime
from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    document_id: str | None = None
    note_type: str = "manual"
    title: str = Field(min_length=1)
    body_markdown: str = Field(min_length=1)
    source_type: str = "manual"
    epistemic_type: str = "fact"
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class NoteUpdate(BaseModel):
    title: str | None = None
    body_markdown: str | None = None
    status: str | None = None
    epistemic_type: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class NoteRead(BaseModel):
    id: str
    document_id: str | None
    note_type: str
    title: str
    body_markdown: str
    source_type: str
    status: str
    epistemic_type: str
    confidence: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
