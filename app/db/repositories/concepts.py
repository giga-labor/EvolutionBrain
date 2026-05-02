from sqlalchemy.orm import Session
from app.db.models import Concept


class ConceptRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0) -> list[Concept]:
        return self.db.query(Concept).offset(offset).limit(limit).all()

    def get(self, id: str) -> Concept | None:
        return self.db.get(Concept, id)

    def create(self, **kwargs) -> Concept:
        item = Concept(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, id: str, **kwargs) -> Concept | None:
        item = self.db.get(Concept, id)
        if not item:
            return None
        for k, v in kwargs.items():
            setattr(item, k, v)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, id: str) -> bool:
        item = self.db.get(Concept, id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
