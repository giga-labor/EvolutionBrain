from sqlalchemy.orm import Session
from app.db.models import Project


class ProjectRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0) -> list[Project]:
        return self.db.query(Project).offset(offset).limit(limit).all()

    def get(self, id: str) -> Project | None:
        return self.db.get(Project, id)

    def create(self, **kwargs) -> Project:
        project = Project(**kwargs)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def update(self, id: str, **kwargs) -> Project | None:
        project = self.db.get(Project, id)
        if not project:
            return None
        for k, v in kwargs.items():
            setattr(project, k, v)
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, id: str) -> bool:
        project = self.db.get(Project, id)
        if not project:
            return False
        self.db.delete(project)
        self.db.commit()
        return True
