from sqlalchemy.orm import Session
from app.db.models import Job


class JobRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0) -> list[Job]:
        return self.db.query(Job).order_by(Job.priority.desc()).offset(offset).limit(limit).all()

    def get(self, id: str) -> Job | None:
        return self.db.get(Job, id)

    def create(self, **kwargs) -> Job:
        job = Job(**kwargs)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def update_status(self, id: str, status: str) -> Job | None:
        job = self.db.get(Job, id)
        if not job:
            return None
        job.status = status
        self.db.commit()
        self.db.refresh(job)
        return job

    def delete(self, id: str) -> bool:
        job = self.db.get(Job, id)
        if not job:
            return False
        self.db.delete(job)
        self.db.commit()
        return True
