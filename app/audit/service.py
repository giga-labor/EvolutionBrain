from sqlalchemy.orm import Session
from app.db.repositories.audit import AuditRepo


class AuditService:
    def __init__(self, db: Session):
        self.repo = AuditRepo(db)

    def log(
        self,
        entity_type: str,
        entity_id: str,
        action: str,
        payload: dict | None = None,
        actor: str | None = None,
    ) -> None:
        self.repo.log(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            payload=payload,
            actor=actor,
        )
