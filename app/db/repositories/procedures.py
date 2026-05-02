from sqlalchemy.orm import Session
from app.db.models import Procedure


class ProcedureRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0) -> list[Procedure]:
        return self.db.query(Procedure).offset(offset).limit(limit).all()

    def get(self, id: str) -> Procedure | None:
        return self.db.get(Procedure, id)

    def create(self, **kwargs) -> Procedure:
        item = Procedure(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, id: str, **kwargs) -> Procedure | None:
        item = self.db.get(Procedure, id)
        if not item:
            return None
        for k, v in kwargs.items():
            setattr(item, k, v)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, id: str) -> bool:
        item = self.db.get(Procedure, id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
