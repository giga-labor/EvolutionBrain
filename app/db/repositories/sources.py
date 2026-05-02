from sqlalchemy.orm import Session
from app.db.models import SourceProfile


class SourceProfileRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 200, offset: int = 0, source_type: str | None = None) -> list[SourceProfile]:
        q = self.db.query(SourceProfile)
        if source_type:
            q = q.filter(SourceProfile.source_type == source_type)
        return q.order_by(SourceProfile.name.asc()).offset(offset).limit(limit).all()

    def get(self, id: str) -> SourceProfile | None:
        return self.db.get(SourceProfile, id)

    def create(self, **kwargs) -> SourceProfile:
        item = SourceProfile(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, id: str) -> bool:
        item = self.db.get(SourceProfile, id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
