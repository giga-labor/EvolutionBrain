from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.models import MemoryItem


class MemoryItemRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0, layer: str | None = None) -> list[MemoryItem]:
        q = self.db.query(MemoryItem)
        if layer:
            q = q.filter(MemoryItem.layer == layer)
        return q.offset(offset).limit(limit).all()

    def get(self, id: str) -> MemoryItem | None:
        return self.db.get(MemoryItem, id)

    def create(self, **kwargs) -> MemoryItem:
        item = MemoryItem(**kwargs)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, id: str, **kwargs) -> MemoryItem | None:
        item = self.db.get(MemoryItem, id)
        if not item:
            return None
        for k, v in kwargs.items():
            setattr(item, k, v)
        self.db.commit()
        self.db.refresh(item)
        return item

    def touch(self, id: str) -> MemoryItem | None:
        item = self.db.get(MemoryItem, id)
        if not item:
            return None
        item.access_count += 1
        item.last_accessed_at = datetime.now(timezone.utc).isoformat()
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_by_object(self, object_type: str, object_id: str) -> MemoryItem | None:
        return (
            self.db.query(MemoryItem)
            .filter(MemoryItem.object_type == object_type, MemoryItem.object_id == object_id)
            .first()
        )

    def delete(self, id: str) -> bool:
        item = self.db.get(MemoryItem, id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
