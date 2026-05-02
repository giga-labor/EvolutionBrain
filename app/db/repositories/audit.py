import json
from sqlalchemy.orm import Session
from app.db.models import AuditEntry


class AuditRepo:
    def __init__(self, db: Session):
        self.db = db

    def log(
        self,
        entity_type: str,
        entity_id: str,
        action: str,
        payload: dict | None = None,
        actor: str | None = None,
    ) -> AuditEntry:
        entry = AuditEntry(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            actor=actor,
            payload=json.dumps(payload) if payload else None,
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

    def list(
        self,
        entity_type: str | None = None,
        entity_id: str | None = None,
        limit: int = 50,
    ) -> list[AuditEntry]:
        q = self.db.query(AuditEntry).order_by(AuditEntry.created_at.desc())
        if entity_type:
            q = q.filter(AuditEntry.entity_type == entity_type)
        if entity_id:
            q = q.filter(AuditEntry.entity_id == entity_id)
        return q.limit(limit).all()
