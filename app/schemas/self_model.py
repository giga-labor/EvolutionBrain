from datetime import datetime
from pydantic import BaseModel, Field


class SelfModelUpdate(BaseModel):
    self_name: str | None = None
    self_role: str | None = None
    autonomy_level: str | None = None
    current_focus: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class SelfModelRead(BaseModel):
    id: str
    self_name: str
    self_role: str
    autonomy_level: str
    current_focus: str | None
    confidence: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
