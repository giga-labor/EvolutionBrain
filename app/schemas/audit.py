from datetime import datetime
from pydantic import BaseModel


class AuditEntryRead(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    action: str
    actor: str | None
    payload: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
