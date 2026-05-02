from sqlalchemy.orm import Session
from app.db.models import Task


class TaskRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0, project_id: str | None = None) -> list[Task]:
        q = self.db.query(Task)
        if project_id:
            q = q.filter(Task.project_id == project_id)
        return q.order_by(Task.priority.desc()).offset(offset).limit(limit).all()

    def get(self, id: str) -> Task | None:
        return self.db.get(Task, id)

    def create(self, **kwargs) -> Task:
        item = Task(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, id: str, **kwargs) -> Task | None:
        item = self.db.get(Task, id)
        if not item:
            return None
        for k, v in kwargs.items():
            setattr(item, k, v)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, id: str) -> bool:
        item = self.db.get(Task, id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
