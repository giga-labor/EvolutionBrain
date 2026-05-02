from sqlalchemy.orm import Session
from app.db.models import Decision


class DecisionRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0, project_id: str | None = None) -> list[Decision]:
        q = self.db.query(Decision)
        if project_id:
            q = q.filter(Decision.project_id == project_id)
        return q.offset(offset).limit(limit).all()

    def get(self, id: str) -> Decision | None:
        return self.db.get(Decision, id)

    def create(self, **kwargs) -> Decision:
        item = Decision(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, id: str, **kwargs) -> Decision | None:
        item = self.db.get(Decision, id)
        if not item:
            return None
        for k, v in kwargs.items():
            setattr(item, k, v)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, id: str) -> bool:
        item = self.db.get(Decision, id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
