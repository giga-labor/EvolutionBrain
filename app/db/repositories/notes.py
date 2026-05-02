from sqlalchemy.orm import Session
from app.db.models import Note


class NoteRepo:
    def __init__(self, db: Session):
        self.db = db

    def list(
        self,
        limit: int = 100,
        offset: int = 0,
        document_id: str | None = None,
        include_quarantined: bool = False,
    ) -> list[Note]:
        q = self.db.query(Note)
        if document_id:
            q = q.filter(Note.document_id == document_id)
        if not include_quarantined:
            q = q.filter(Note.status != "quarantined")
        return q.offset(offset).limit(limit).all()

    def get(self, id: str) -> Note | None:
        return self.db.get(Note, id)

    def create(self, **kwargs) -> Note:
        note = Note(**kwargs)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update(self, id: str, **kwargs) -> Note | None:
        note = self.db.get(Note, id)
        if not note:
            return None
        for k, v in kwargs.items():
            setattr(note, k, v)
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete(self, id: str) -> bool:
        note = self.db.get(Note, id)
        if not note:
            return False
        self.db.delete(note)
        self.db.commit()
        return True
