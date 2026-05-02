from sqlalchemy.orm import Session
from app.db.models import Episode


class EpisodeRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0) -> list[Episode]:
        return self.db.query(Episode).offset(offset).limit(limit).all()

    def get(self, id: str) -> Episode | None:
        return self.db.get(Episode, id)

    def create(self, **kwargs) -> Episode:
        item = Episode(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, id: str, **kwargs) -> Episode | None:
        item = self.db.get(Episode, id)
        if not item:
            return None
        for k, v in kwargs.items():
            setattr(item, k, v)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, id: str) -> bool:
        item = self.db.get(Episode, id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
