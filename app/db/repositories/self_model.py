from sqlalchemy.orm import Session
from app.db.models import SelfModel


class SelfModelRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_singleton(self) -> SelfModel:
        item = self.db.query(SelfModel).first()
        if not item:
            item = SelfModel()
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
        return item

    def update_singleton(self, **kwargs) -> SelfModel:
        item = self.get_singleton()
        for k, v in kwargs.items():
            setattr(item, k, v)
        self.db.commit()
        self.db.refresh(item)
        return item
