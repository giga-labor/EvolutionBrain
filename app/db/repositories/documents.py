from sqlalchemy.orm import Session
from app.db.models import Document


class DocumentRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 100, offset: int = 0) -> list[Document]:
        return self.db.query(Document).offset(offset).limit(limit).all()

    def get(self, id: str) -> Document | None:
        return self.db.get(Document, id)

    def get_by_hash(self, content_hash: str) -> Document | None:
        return self.db.query(Document).filter(Document.content_hash == content_hash).first()

    def create(self, **kwargs) -> Document:
        doc = Document(**kwargs)
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def update(self, id: str, **kwargs) -> Document | None:
        doc = self.db.get(Document, id)
        if not doc:
            return None
        for k, v in kwargs.items():
            setattr(doc, k, v)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def delete(self, id: str) -> bool:
        doc = self.db.get(Document, id)
        if not doc:
            return False
        self.db.delete(doc)
        self.db.commit()
        return True
