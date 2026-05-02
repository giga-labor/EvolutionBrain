from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.models import Document, Note, Concept


class RetrievalService:
    def __init__(self, db: Session):
        self.db = db

    _STOPWORDS = {
        "il", "lo", "la", "i", "gli", "le", "un", "una", "uno", "di", "a", "da", "in", "con", "su", "per", "tra",
        "fra", "e", "o", "che", "chi", "cui", "del", "della", "dello", "dei", "degli", "delle", "al", "alla",
        "allo", "ai", "agli", "alle", "nel", "nella", "nello", "nei", "negli", "nelle", "mi", "ti", "si", "ci",
        "vi", "io", "tu", "lui", "lei", "noi", "voi", "loro", "my", "your", "the", "is", "are", "of", "to",
    }

    @staticmethod
    def _tokenize(value: str) -> set[str]:
        raw = "".join(ch.lower() if ch.isalnum() else " " for ch in value).split()
        return {p for p in raw if len(p) >= 3 and p not in RetrievalService._STOPWORDS}

    def keyword_search(self, query: str, limit: int = 20) -> dict:
        if not query.strip():
            return {"query": query, "mode": "keyword", "results": [], "total": 0}

        q = f"%{query}%"

        docs = (
            self.db.query(Document)
            .filter(or_(Document.title.ilike(q), Document.raw_content.ilike(q)))
            .limit(limit)
            .all()
        )
        notes = (
            self.db.query(Note)
            .filter(Note.status != "quarantined")
            .filter(or_(Note.title.ilike(q), Note.body_markdown.ilike(q)))
            .limit(limit)
            .all()
        )

        concepts = (
            self.db.query(Concept)
            .filter(or_(Concept.name.ilike(q), Concept.description.ilike(q)))
            .limit(limit)
            .all()
        )

        results = (
            [{"type": "document", "id": d.id, "title": d.title, "score": 1.0} for d in docs]
            + [{"type": "note", "id": n.id, "title": n.title, "score": 1.0} for n in notes]
            + [{"type": "concept", "id": c.id, "title": c.name, "score": 1.0} for c in concepts]
        )

        return {
            "query": query,
            "mode": "keyword",
            "results": results,
            "total": len(results),
        }

    def semantic_search(self, query: str, limit: int = 20) -> dict:
        tokens = self._tokenize(query)
        if not tokens:
            return {"query": query, "mode": "semantic", "results": [], "total": 0}

        scored: list[dict] = []
        docs = self.db.query(Document).limit(max(limit * 5, 50)).all()
        notes = (
            self.db.query(Note)
            .filter(Note.status != "quarantined")
            .limit(max(limit * 5, 50))
            .all()
        )
        concepts = self.db.query(Concept).limit(max(limit * 5, 50)).all()

        for d in docs:
            hay = f"{d.title or ''} {d.raw_content or ''}"
            ht = self._tokenize(hay)
            overlap = len(tokens & ht)
            if overlap:
                score = overlap / max(len(tokens), 1)
                scored.append({"type": "document", "id": d.id, "title": d.title, "score": round(score, 4)})

        for n in notes:
            hay = f"{n.title} {n.body_markdown}"
            ht = self._tokenize(hay)
            overlap = len(tokens & ht)
            if overlap:
                score = overlap / max(len(tokens), 1)
                scored.append({"type": "note", "id": n.id, "title": n.title, "score": round(score, 4)})

        for c in concepts:
            hay = f"{c.name} {c.description or ''}"
            ht = self._tokenize(hay)
            overlap = len(tokens & ht)
            if overlap:
                score = overlap / max(len(tokens), 1)
                scored.append({"type": "concept", "id": c.id, "title": c.name, "score": round(score, 4)})

        scored.sort(key=lambda x: x["score"], reverse=True)
        top = scored[:limit]
        return {"query": query, "mode": "semantic", "results": top, "total": len(top)}

    def hybrid_search(self, query: str, limit: int = 20) -> dict:
        kw = self.keyword_search(query, limit=limit)
        sem = self.semantic_search(query, limit=limit)

        merged: dict[tuple[str, str], dict] = {}
        for item in kw["results"]:
            key = (item["type"], item["id"])
            merged[key] = {**item, "score": round(item["score"] * 0.55, 4)}
        for item in sem["results"]:
            key = (item["type"], item["id"])
            if key in merged:
                merged[key]["score"] = round(merged[key]["score"] + item["score"] * 0.45, 4)
            else:
                merged[key] = {**item, "score": round(item["score"] * 0.45, 4)}

        results = sorted(merged.values(), key=lambda x: x["score"], reverse=True)[:limit]
        return {"query": query, "mode": "hybrid", "results": results, "total": len(results)}

    def search(self, query: str, mode: str = "hybrid", limit: int = 20) -> dict:
        if mode == "keyword":
            return self.keyword_search(query, limit=limit)
        if mode == "semantic":
            return self.semantic_search(query, limit=limit)
        return self.hybrid_search(query, limit=limit)
