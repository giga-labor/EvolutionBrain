from sqlalchemy.orm import Session
from app.db.models import Relation


class RelationRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0) -> list[Relation]:
        return self.db.query(Relation).offset(offset).limit(limit).all()

    def get(self, id: str) -> Relation | None:
        return self.db.get(Relation, id)

    def create(self, **kwargs) -> Relation:
        item = Relation(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, id: str, **kwargs) -> Relation | None:
        item = self.db.get(Relation, id)
        if not item:
            return None
        for k, v in kwargs.items():
            setattr(item, k, v)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, id: str) -> bool:
        item = self.db.get(Relation, id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
