from sqlalchemy.orm import Session
from app.db.models import SystemState


class SystemStateRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_singleton(self) -> SystemState:
        item = self.db.query(SystemState).first()
        if not item:
            item = SystemState()
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
        return item

    def update_singleton(self, **kwargs) -> SystemState:
        item = self.get_singleton()
        for k, v in kwargs.items():
            setattr(item, k, v)
        self.db.commit()
        self.db.refresh(item)
        return item
