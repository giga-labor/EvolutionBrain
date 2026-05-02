from sqlalchemy.orm import Session
from app.db.models import Goal


class GoalRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0, project_id: str | None = None) -> list[Goal]:
        q = self.db.query(Goal)
        if project_id:
            q = q.filter(Goal.project_id == project_id)
        return q.order_by(Goal.priority.desc()).offset(offset).limit(limit).all()

    def get(self, id: str) -> Goal | None:
        return self.db.get(Goal, id)

    def create(self, **kwargs) -> Goal:
        item = Goal(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, id: str, **kwargs) -> Goal | None:
        item = self.db.get(Goal, id)
        if not item:
            return None
        for k, v in kwargs.items():
            setattr(item, k, v)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, id: str) -> bool:
        item = self.db.get(Goal, id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
