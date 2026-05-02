from sqlalchemy.orm import Session
from app.schemas.chat import ChatQueryRequest, ChatResponse
from app.retrieval.service import RetrievalService
from app.attention.service import AttentionService
from app.metacognition.service import MetacognitionService
from app.db.models import Note, Document, Concept
from app.db.repositories.notes import NoteRepo
from app.db.repositories.tasks import TaskRepo
from app.audit.service import AuditService
import re
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, date
import json


class ReasoningService:
    # Brain-first policy: prefer compact internal memory answers before broad retrieval.
    _BRAIN_FIRST_MAX_NOTES = 120
    _BRAIN_FIRST_MIN_SCORE = 0.75
    _RETRIEVAL_FALLBACK_LIMIT = 3
    _BRAIN_GLOBAL_LIMIT = 2
    _BRAIN_GLOBAL_MIN_SCORE = 0.1
    _COMMAND_REGISTRY = [
        {
            "name": "cerca",
            "syntax": "cerca: <query>",
            "description": "Cerca nelle conoscenze interne di Ebby.",
            "risk": "read_only",
        },
        {
            "name": "cerca comando",
            "syntax": "cerca comando: <query>",
            "description": "Cerca tra funzioni e comandi disponibili nella chat.",
            "risk": "read_only",
        },
        {
            "name": "cerca internet",
            "syntax": "cerca internet: <query>",
            "description": "Prepara una ricerca web. Richiede conferma amministratore per eseguirla.",
            "risk": "external_read",
        },
        {
            "name": "autorizzo ricerca internet",
            "syntax": "autorizzo ricerca internet: <query>",
            "description": "Esegue una ricerca web supervisionata e restituisce risultati sintetici.",
            "risk": "external_read_confirmed",
        },
        {
            "name": "pianifica azione",
            "syntax": "pianifica azione: {json}",
            "description": "Valuta rischio e impatto di una azione agentica senza eseguirla.",
            "risk": "plan_only",
        },
        {
            "name": "esegui azione autorizzata",
            "syntax": "esegui azione autorizzata: {json}",
            "description": "Esegue una azione reale tramite ActionService con conferma amministratore.",
            "risk": "admin_confirmed_write",
        },
        {
            "name": "importa URL",
            "syntax": "importa https://...",
            "description": "Importa contenuto da URL come documento interno.",
            "risk": "external_read_write_memory",
        },
        {
            "name": "crea nota",
            "syntax": "crea nota: <testo>",
            "description": "Crea una nota manuale.",
            "risk": "write_memory",
        },
        {
            "name": "crea task",
            "syntax": "crea task: <titolo>",
            "description": "Crea un task operativo.",
            "risk": "write_task",
        },
        {
            "name": "backup",
            "syntax": "backup",
            "description": "Crea un backup del database.",
            "risk": "maintenance",
        },
        {
            "name": "help ebby",
            "syntax": "help ebby | help ebby completo | help ebby attivazione",
            "description": "Mostra l'auto-aiuto interno di Ebby: attivazione LLM, canali, limiti e protocollo operativo.",
            "risk": "read_only",
        },
    ]
    _Q_STOP = {
        "come", "quando", "dove", "quanto", "quanti", "quale", "qual", "chi", "cosa", "cosa", "che",
        "il", "lo", "la", "i", "gli", "le", "un", "una", "uno", "del", "della", "dei", "degli", "delle",
        "di", "a", "da", "in", "con", "su", "per", "tra", "fra", "e", "mi", "mio", "mia", "mie", "miei",
        "ho", "sono", "sei", "si", "tu", "io",
    }
    _TOKEN_ALIASES = {
        "chiamo": "nome",
    }
    def __init__(self, db: Session):
        self.db = db
        self.retrieval = RetrievalService(db)
        self.attention = AttentionService()
        self.metacognition = MetacognitionService()
        self.note_repo = NoteRepo(db)
        self.task_repo = TaskRepo(db)
        self.audit = AuditService(db)

    @staticmethod
    def _tokens(message: str) -> set[str]:
        return {p for p in "".join(ch.lower() if ch.isalnum() else " " for ch in (message or "")).split() if p}

    @staticmethod
    def _norm(value: str) -> str:
        return " ".join((value or "").strip().lower().split())

    def _tok_norm(self, value: str) -> set[str]:
        raw = [p for p in re.split(r"[^a-z0-9]+", self._norm(value)) if p]
        out = set()
        for t in raw:
            if len(t) < 2 or t in self._Q_STOP:
                continue
            out.add(self._TOKEN_ALIASES.get(t, t))
        return out

    def _kv_title(self, subject: str, attribute: str) -> str:
        return f"KV::{self._norm(subject)}::{self._norm(attribute)}"

    def _upsert_kv(self, subject: str, attribute: str, value: str) -> tuple[str, str]:
        title = self._kv_title(subject, attribute)
        body = f"{subject} | {attribute} | {value}"
        existing = (
            self.db.query(Note)
            .filter(Note.title == title, Note.status == "active")
            .order_by(Note.updated_at.desc())
            .first()
        )
        if existing:
            if (existing.body_markdown or "").strip() == body:
                return ("note_already_known", existing.id)
            n = self.note_repo.update(existing.id, body_markdown=body, status="active", confidence=1.0)
            return ("note_updated", n.id)
        n = self.note_repo.create(
            note_type="profile_kv",
            title=title,
            body_markdown=body,
            source_type="chat",
            epistemic_type="fact",
            confidence=1.0,
        )
        return ("note_created", n.id)

    def _lookup_kv(self, subject: str, attribute: str) -> tuple[str, str] | None:
        title = self._kv_title(subject, attribute)
        n = (
            self.db.query(Note)
            .filter(Note.title == title, Note.status == "active")
            .order_by(Note.updated_at.desc())
            .first()
        )
        if not n:
            return None
        parts = [p.strip() for p in (n.body_markdown or "").split("|")]
        if len(parts) >= 3:
            return (parts[2], n.id)
        return None

    def _upsert_generic_fact(self, key: str, value: str) -> tuple[str, str]:
        title = f"KVG::{self._norm(key)}"
        body = f"{key.strip()} | {value.strip()}"
        existing = (
            self.db.query(Note)
            .filter(Note.title == title, Note.status == "active")
            .order_by(Note.updated_at.desc())
            .first()
        )
        if existing:
            if (existing.body_markdown or "").strip() == body:
                return ("note_already_known", existing.id)
            n = self.note_repo.update(existing.id, body_markdown=body, status="active", confidence=1.0)
            return ("note_updated", n.id)
        n = self.note_repo.create(
            note_type="profile_kv_generic",
            title=title,
            body_markdown=body,
            source_type="chat",
            epistemic_type="fact",
            confidence=1.0,
        )
        return ("note_created", n.id)

    def _lookup_generic_fact(self, key: str) -> tuple[str, str] | None:
        title = f"KVG::{self._norm(key)}"
        n = (
            self.db.query(Note)
            .filter(Note.title == title, Note.status == "active")
            .order_by(Note.updated_at.desc())
            .first()
        )
        if not n:
            return None
        parts = [p.strip() for p in (n.body_markdown or "").split("|")]
        if len(parts) >= 2:
            return (parts[1], n.id)
        return None

    def _lookup_generic_fact_fuzzy(self, query: str) -> tuple[str, str] | None:
        qtok = self._tok_norm(query)
        if not qtok:
            return None
        notes = (
            self.db.query(Note)
            .filter(Note.note_type == "profile_kv_generic", Note.status == "active")
            .all()
        )
        best = None
        best_score = 0.0
        for n in notes:
            parts = [p.strip() for p in (n.body_markdown or "").split("|")]
            if len(parts) < 2:
                continue
            key = parts[0]
            value = parts[1]
            ktok = self._tok_norm(key)
            if not ktok:
                continue
            overlap = len(qtok & ktok)
            if overlap == 0:
                continue
            score = overlap / max(len(ktok), 1)
            if score > best_score:
                best_score = score
                best = (value, n.id)
        if best and best_score >= 0.34:
            return best
        return None

    def _lookup_generic_fact_aliases(self, keys: list[str]) -> tuple[str, str] | None:
        for k in keys:
            hit = self._lookup_generic_fact(k)
            if hit:
                return hit
        return None

    def _search_command_registry(self, query: str | None = None) -> list[dict]:
        if not query:
            return self._COMMAND_REGISTRY
        qtok = self._tok_norm(query)
        if not qtok:
            return self._COMMAND_REGISTRY
        scored: list[tuple[int, dict]] = []
        for command in self._COMMAND_REGISTRY:
            hay = f"{command['name']} {command['syntax']} {command['description']} {command['risk']}"
            score = len(qtok & self._tok_norm(hay))
            if score:
                scored.append((score, command))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [item for _, item in scored]

    @staticmethod
    def _format_command_registry(commands: list[dict]) -> str:
        if not commands:
            return "Nessun comando trovato."
        lines = ["Comandi disponibili:"]
        for command in commands:
            lines.append(
                f"- {command['syntax']} | rischio={command['risk']} | {command['description']}"
            )
        return "\n".join(lines)

    @staticmethod
    def _parse_action_json(raw: str) -> tuple[dict | None, str | None]:
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            return None, f"JSON non valido: {exc}"
        if not isinstance(value, dict):
            return None, "La richiesta azione deve essere un oggetto JSON."
        return value, None

    def _web_search(self, query: str, limit: int = 5) -> dict:
        encoded = urllib.parse.urlencode({"q": query})
        url = f"https://duckduckgo.com/html/?{encoded}"
        req = urllib.request.Request(url, headers={"User-Agent": "EvoBrain/1.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read(500_000).decode("utf-8", errors="ignore")
        results = []
        pattern = re.compile(
            r'class="result__a"[^>]*href="(?P<href>[^"]+)"[^>]*>(?P<title>.*?)</a>',
            re.IGNORECASE | re.DOTALL,
        )
        for match in pattern.finditer(html):
            title = re.sub(r"<[^>]+>", " ", match.group("title"))
            title = re.sub(r"\s+", " ", urllib.parse.unquote(title)).strip()
            href = urllib.parse.unquote(match.group("href")).strip()
            if title and href:
                results.append({"title": title, "url": href})
            if len(results) >= limit:
                break
        return {"query": query, "results": results, "source": "duckduckgo_html"}

    def _looks_like_agentic_request(self, message: str) -> bool:
        text = (message or "").strip()
        if not text or text.endswith("?"):
            return False
        low = text.lower()
        first = low.split()[0] if low.split() else ""
        if first in {"ciao", "buongiorno", "buonasera", "ok", "okay", "grazie"}:
            return False
        starters = {
            "apri", "chiudi", "pulisci", "cancella", "mostra", "nascondi", "esegui",
            "avvia", "ferma", "crea", "aggiungi", "modifica", "sistema", "risolvi",
            "implementa", "configura", "installa", "scarica", "importa", "connetti",
            "trova", "cerca", "analizza", "genera", "aggiorna", "abilita", "disabilita",
        }
        if first in starters:
            return True
        # Short command-like utterances often omit verbs, for example "fullscreen".
        return len(low.split()) <= 4 and not any(ch in low for ch in ".:,;")

    def _agentic_capability_response(self, payload: ChatQueryRequest) -> ChatResponse | None:
        message = (payload.message or "").strip()
        if not self._looks_like_agentic_request(message):
            return None

        command_hits = self._search_command_registry(message)[:5]
        strong_hits = [
            c for c in command_hits
            if len(self._tok_norm(message) & self._tok_norm(f"{c['name']} {c['syntax']}")) > 0
        ]

        web_results: list[dict] = []
        web_note = "Ricerca internet non eseguita: serve allow_external_sources=true o autorizzazione esplicita."
        if payload.allow_external_sources:
            try:
                web = self._web_search(f"how to implement command {message} in web app", limit=3)
                web_results = web.get("results", [])
                web_note = f"Ricerca internet eseguita: {len(web_results)} risultati."
            except Exception as exc:
                web_note = f"Ricerca internet tentata ma fallita: {exc}"

        plan = {
            "type": "agentic_capability_plan",
            "request": message,
            "interpretation": "Richiesta operativa/capacita da risolvere, mappare o implementare.",
            "local_command_matches": strong_hits,
            "web_search": {
                "performed": bool(payload.allow_external_sources),
                "note": web_note,
                "results": web_results,
            },
            "implementation_policy": {
                "can_plan_autonomously": True,
                "can_modify_code": False,
                "code_changes_require_admin_authorization": True,
                "destructive_actions_require_admin_authorization": True,
            },
            "next_steps": [
                "Definire comportamento atteso e superficie comando.",
                "Verificare se una funzione esistente copre gia la richiesta.",
                "Se manca, aggiungere handler dedicato o capability registrata.",
                "Eseguire test/smoke test prima di considerarla disponibile.",
            ],
        }

        if strong_hits:
            lines = ["Ho trovato funzioni/comandi potenzialmente rilevanti:"]
            for command in strong_hits:
                lines.append(f"- {command['syntax']} | {command['description']}")
        else:
            lines = [
                "Ho interpretato il messaggio come richiesta operativa non ancora mappata a un comando esistente.",
                "Posso preparare l'implementazione, ma le modifiche al codice richiedono autorizzazione amministratore.",
            ]
        lines.append(web_note)
        lines.append("Prossimo comando utile: pianifica azione: {\"type\":\"create_task\",\"payload\":{\"title\":\"Implementare capability chat: " + message.replace('"', "'")[:120] + "\"}}")

        return ChatResponse(
            answer="\n".join(lines),
            epistemic_type="agentic_plan",
            confidence=0.75 if strong_hits else 0.55,
            used_sources=[{"object_type": "web", **item} for item in web_results],
            used_objects=[],
            suggested_actions=[plan],
            executed_actions=[],
            active_mode="agentic_interpreter",
            context_summary="Richiesta operativa interpretata come capability agentica.",
        )

    def _extract_kv_from_statement(self, msg: str) -> tuple[str, str, str] | None:
        text = (msg or "").strip()
        low = text.lower()
        # "il modello lexus che ho è UX250H" / "modello lexus è UX250H"
        m = re.search(r"\b(modello|targa|scadenza|revisione)\s+([a-z0-9]+(?:\s+[a-z0-9]+)*)\s+(?:che ho\s+)?(?:e|è)\s+([a-z0-9\-\/]+)\b", low)
        if m:
            return (m.group(2).strip(), m.group(1).strip(), text[m.start(3):].strip())
        # "la targa della mia lexus ux250h è GJ039YV"
        m2 = re.search(r"\b(?:il|la)\s+(modello|targa)\s+(?:della|del)\s+(?:mia|mio)\s+([a-z0-9]+(?:\s+[a-z0-9]+)*)\s+(?:e|è)\s+([a-z0-9\-\/]+)\b", low)
        if m2:
            return (m2.group(2).strip(), m2.group(1).strip(), text[m2.start(3):].strip())
        return None

    def _extract_kv_query(self, msg: str) -> tuple[str, str] | None:
        text = self._norm(msg)
        # "modello hunday?" / "targa lexus?"
        m = re.search(r"\b(modello|targa|scadenza|revisione)\s+([a-z0-9]+(?:\s+[a-z0-9]+)*)\??$", text)
        if m:
            return (m.group(2).strip(), m.group(1).strip())
        # "qual è il modello della lexus?"
        m2 = re.search(r"\b(modello|targa|scadenza|revisione)\s+(?:della|del)\s+([a-z0-9]+(?:\s+[a-z0-9]+)*)\??$", text)
        if m2:
            return (m2.group(2).strip(), m2.group(1).strip())
        return None

    def _extract_generic_fact_statement(self, msg: str) -> tuple[str, str] | None:
        text = (msg or "").strip()
        if not text or text.endswith("?"):
            return None
        # generic "X è Y" / "X e Y" (ASCII fallback) / "X = Y"
        m = re.search(r"^\s*(.{2,120}?)\s+(?:=|è|e)\s+(.{1,180})\s*$", text, re.IGNORECASE)
        if not m:
            return None
        left = m.group(1).strip(" .,:;")
        right = m.group(2).strip(" .,:;")
        if len(left) < 2 or len(right) < 1:
            return None
        return (left, right)

    def _extract_generic_fact_query(self, msg: str) -> str | None:
        text = (msg or "").strip().rstrip("?").strip()
        if not text:
            return None
        low = self._norm(text)
        # "qual è X" / "cos'è X" / "cosa è X"
        for pfx in ["qual e ", "qual è ", "cos e ", "cos'è ", "cosa e ", "cosa è "]:
            if low.startswith(pfx):
                candidate = text[len(pfx):].strip()
                if len(candidate) >= 2:
                    return candidate
        # short direct query "x y z?"
        if len(low.split()) <= 6:
            return text
        return None

    @staticmethod
    def _memory_payload_from_explicit_request(msg: str) -> str | None:
        text = (msg or "").strip()
        patterns = [
            r"^(?:ricorda|memorizza|salva|impara|consolida)\s+(?:che\s+)?(.+)$",
            r"^(?:tieni a mente|segna)\s+(?:che\s+)?(.+)$",
            r"^(?:nota conoscenza|conoscenza)[:\s]+(.+)$",
        ]
        for pattern in patterns:
            match = re.match(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                payload = match.group(1).strip()
                return payload if len(payload) >= 3 else None
        return None

    @staticmethod
    def _knowledge_fingerprint(value: str) -> str:
        return " ".join(re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).split())

    def _find_equivalent_active_note(self, body: str) -> Note | None:
        needle = self._knowledge_fingerprint(body)
        if not needle:
            return None
        notes = (
            self.db.query(Note)
            .filter(
                Note.status == "active",
                Note.note_type.in_(["chat_fact", "profile", "profile_kv", "profile_kv_generic"]),
            )
            .all()
        )
        for note in notes:
            hay = self._knowledge_fingerprint(f"{note.title} {note.body_markdown or ''}")
            if needle and (needle == hay or needle in hay):
                return note
        return None

    def _create_explicit_memory_note(self, body: str) -> dict:
        existing = self._find_equivalent_active_note(body)
        if existing:
            return {"type": "note_already_known", "id": existing.id}
        title = f"Info esplicita da chat {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        note = self.note_repo.create(
            note_type="chat_fact",
            title=title,
            body_markdown=body,
            source_type="chat",
            epistemic_type="fact",
            confidence=0.95,
        )
        self.audit.log("note", note.id, "created_from_explicit_chat_memory", {"message": body})
        return {"type": "note_created", "id": note.id}

    def _extract_generic_fact_statement(self, msg: str) -> tuple[str, str] | None:
        text = (msg or "").strip()
        if not text or text.endswith("?"):
            return None
        name_match = re.search(r"^\s*mi\s+chiamo\s+(.{2,80})\s*$", text, re.IGNORECASE)
        if name_match:
            return ("il mio nome", name_match.group(1).strip(" .,:;"))
        spouse_match = re.search(r"^\s*mia\s+moglie\s+si\s+chiama\s+(.{2,80})\s*$", text, re.IGNORECASE)
        if spouse_match:
            return ("mia moglie", spouse_match.group(1).strip(" .,:;"))
        birthday_match = re.search(r"^\s*(.{2,80}?)\s+fa\s+il\s+compleanno\s+il\s+(.{6,40})\s*$", text, re.IGNORECASE)
        if birthday_match:
            return (f"compleanno {birthday_match.group(1).strip(' .,:;')}", birthday_match.group(2).strip(" .,:;"))
        match = re.search(r"^\s*(.{2,120}?)\s+(?:=|e|è)\s+(.{1,180})\s*$", text, re.IGNORECASE)
        if not match:
            return None
        left = match.group(1).strip(" .,:;")
        right = match.group(2).strip(" .,:;")
        if len(left) < 2 or len(right) < 1:
            return None
        return (left, right)

    def _extract_vehicle_profile_statement(self, msg: str) -> tuple[str, str] | None:
        text = (msg or "").strip()
        if not text or text.endswith("?"):
            return None
        match = re.search(
            r"\bho(?:\s+anche)?\s+(?:una|un|1|2|due)?\s*(?:auto|macchina|veicolo)?\s*(lexus|hunday|hyundai|toyota|fiat|alfa|bmw|mercedes|audi|ford|renault|peugeot|citroen|volkswagen)\s+([a-z0-9][a-z0-9\- ]{1,40})\b",
            text,
            re.IGNORECASE,
        )
        if not match:
            return None
        brand = match.group(1).strip()
        model = " ".join(match.group(2).strip(" .,:;").split())
        if brand.lower() in {"hunday", "hyundai"}:
            brand = "Hyundai"
        else:
            brand = brand[:1].upper() + brand[1:]
        return brand, model

    def _upsert_vehicle_profile(self, brand: str, model: str) -> tuple[str, str]:
        title = f"Profilo veicolo: {brand} {model}"
        body = f"Veicolo utente: {brand} {model}."
        existing = (
            self.db.query(Note)
            .filter(Note.title == title, Note.status == "active")
            .order_by(Note.updated_at.desc())
            .first()
        )
        if existing:
            if (existing.body_markdown or "").strip() == body:
                return ("note_already_known", existing.id)
            n = self.note_repo.update(existing.id, body_markdown=body, status="active", confidence=1.0)
            return ("note_updated", n.id)
        n = self.note_repo.create(
            note_type="profile",
            title=title,
            body_markdown=body,
            source_type="chat",
            epistemic_type="fact",
            confidence=1.0,
        )
        return ("note_created", n.id)

    def _lookup_chat_facts(self, query: str) -> ChatResponse | None:
        """Cerca nei chat_fact salvati per rispondere a domande personali brevi."""
        qtok = self._tok_norm(query)
        if not qtok:
            return None
        notes = (
            self.db.query(Note)
            .filter(
                Note.note_type.in_(["chat_fact", "profile_kv_generic", "profile"]),
                Note.status == "active",
            )
            .order_by(Note.updated_at.desc())
            .limit(500)
            .all()
        )
        best_score = 0.0
        best_note = None
        for n in notes:
            body = (n.body_markdown or "").strip()
            if not body:
                continue
            btok = self._tok_norm(body)
            if not btok:
                continue
            overlap = len(qtok & btok)
            if overlap == 0:
                continue
            score = overlap / max(len(qtok), 1)
            if score > best_score:
                best_score = score
                best_note = n
        if best_note and best_score >= 0.35:
            return ChatResponse(
                answer=best_note.body_markdown or "",
                epistemic_type="fact",
                confidence=round(min(1.0, best_note.confidence * best_score + 0.3), 2),
                used_sources=[{"object_type": "note", "object_id": best_note.id, "title": best_note.title, "score": best_score}],
                used_objects=[{"object_type": "note", "object_id": best_note.id, "title": best_note.title}],
                suggested_actions=[],
                executed_actions=[],
                active_mode="profile_memory",
                context_summary="Risposta da chat_fact.",
            )
        return None

    def _answer_from_profile_memory(self, message: str) -> ChatResponse | None:
        tokens = self._tokens(message)
        if not tokens:
            return None

        def _note_by_title(title: str) -> Note | None:
            return (
                self.db.query(Note)
                .filter(Note.title == title, Note.status == "active")
                .order_by(Note.updated_at.desc())
                .first()
            )

        if any(t in tokens for t in {"chiami", "nome"}) and any(t in tokens for t in {"ti", "tu", "tuo"}):
            n = _note_by_title("Profilo EvoBrain: identita") or _note_by_title("Profilo EvoBrain: nomignolo")
            if n:
                return ChatResponse(
                    answer="Ebby",
                    epistemic_type="fact",
                    confidence=min(1.0, n.confidence),
                    used_sources=[{"object_type": "note", "object_id": n.id, "title": n.title, "score": n.confidence}],
                    used_objects=[{"object_type": "note", "object_id": n.id, "title": n.title}],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="profile_memory",
                    context_summary="Identita conversazionale da profilo.",
                )

        # Birthday countdown intent
        if "compleanno" in tokens and any(t in tokens for t in {"giorni", "mancano", "quanto", "quanti"}):
            n = _note_by_title("Anagrafica: Compleanno")
            if n:
                iso = self._parse_it_date(n.body_markdown or "")
                if iso:
                    y, m, d = [int(x) for x in iso.split("-")]
                    today = date.today()
                    next_bday = date(today.year, m, d)
                    if next_bday < today:
                        next_bday = date(today.year + 1, m, d)
                    days_left = (next_bday - today).days
                    return ChatResponse(
                        answer=f"{days_left} giorni",
                        epistemic_type="fact",
                        confidence=min(1.0, n.confidence),
                        used_sources=[{"object_type": "note", "object_id": n.id, "title": n.title, "score": n.confidence}],
                        used_objects=[{"object_type": "note", "object_id": n.id, "title": n.title}],
                        suggested_actions=[],
                        executed_actions=[],
                        active_mode="profile_memory",
                        context_summary="Countdown compleanno da memoria profilo.",
                    )

        # Birthday date intent
        if any(t in tokens for t in {"compleanno", "nascita", "birthday"}):
            n = _note_by_title("Anagrafica: Compleanno")
            if n:
                return ChatResponse(
                    answer=n.body_markdown.replace("Data di nascita utente: ", "").strip().rstrip("."),
                    epistemic_type="fact",
                    confidence=min(1.0, n.confidence),
                    used_sources=[{"object_type": "note", "object_id": n.id, "title": n.title, "score": n.confidence}],
                    used_objects=[{"object_type": "note", "object_id": n.id, "title": n.title}],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="profile_memory",
                    context_summary="Risposta da memoria profilo utente.",
                )

        # Vehicle revision due date intent
        if ("revisione" in tokens and any(t in tokens for t in {"scade", "scadenza", "quando", "data"})) or (
            "data" in tokens and len(tokens) <= 3
        ):
            due_iso = self._find_vehicle_revision_due_date()
            if due_iso:
                return ChatResponse(
                    answer=due_iso,
                    epistemic_type="fact",
                    confidence=0.95,
                    used_sources=[],
                    used_objects=[],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="profile_memory",
                    context_summary="Scadenza revisione da task/knowledge interna.",
                )

        # Vehicle intent — solo se chiede del modello/tipo, non della quantità
        _quantity_tokens = {"quante", "quanti", "quanto", "numero", "ho", "possiedo", "mie", "miei"}
        if (
            any(t in tokens for t in {"auto", "macchina", "veicolo"})
            and "revisione" not in tokens
            and not any(t in tokens for t in _quantity_tokens)
        ):
            n = _note_by_title("Profilo veicolo")
            if n:
                body_l = (n.body_markdown or "").lower()
                if "lexus" in body_l and "ux" in body_l:
                    ans = "Lexus UX"
                else:
                    ans = n.body_markdown
                return ChatResponse(
                    answer=ans,
                    epistemic_type="inferred_fact",
                    confidence=min(1.0, n.confidence),
                    used_sources=[{"object_type": "note", "object_id": n.id, "title": n.title, "score": n.confidence}],
                    used_objects=[{"object_type": "note", "object_id": n.id, "title": n.title}],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="profile_memory",
                    context_summary="Risposta da profilo veicolo utente.",
                )

        # Vehicle plate intent
        if "targa" in tokens and any(t in tokens for t in {"lexus", "auto", "ux250h", "mia", "mio"}):
            n = _note_by_title("Profilo veicolo: targa")
            if n:
                plate = self._extract_plate(n.body_markdown or "")
                if plate:
                    return ChatResponse(
                        answer=plate,
                        epistemic_type="fact",
                        confidence=min(1.0, n.confidence),
                        used_sources=[{"object_type": "note", "object_id": n.id, "title": n.title, "score": n.confidence}],
                        used_objects=[{"object_type": "note", "object_id": n.id, "title": n.title}],
                        suggested_actions=[],
                        executed_actions=[],
                        active_mode="profile_memory",
                        context_summary="Targa veicolo da memoria profilo.",
                    )

        # Cerca nei fatti appresi dalla chat dopo gli intenti specifici.
        chat_fact_answer = self._lookup_chat_facts(message)
        if chat_fact_answer:
            return chat_fact_answer

        # Generic KV query intent (generic auto-learning retrieval)
        kvq = self._extract_kv_query(message)
        if kvq:
            subject, attribute = kvq
            hit = self._lookup_kv(subject, attribute)
            if hit:
                value, note_id = hit
                return ChatResponse(
                    answer=value,
                    epistemic_type="fact",
                    confidence=1.0,
                    used_sources=[{"object_type": "note", "object_id": note_id, "title": self._kv_title(subject, attribute), "score": 1.0}],
                    used_objects=[{"object_type": "note", "object_id": note_id, "title": self._kv_title(subject, attribute)}],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="profile_memory",
                    context_summary="Risposta da memoria KV auto-appresa.",
                )
            # Explicit unknown for direct KV-style questions
            return ChatResponse(
                answer="Non conosco la risposta: non ho ancora quel dato in memoria.",
                epistemic_type="ignorance",
                confidence=0.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[{"type": "ask_more_context"}],
                executed_actions=[],
                active_mode="profile_memory",
                context_summary="KV query senza valore memorizzato.",
            )

        # Generic fact query intent (topic-agnostic)
        gq = self._extract_generic_fact_query(message)
        if gq:
            hit = self._lookup_generic_fact(gq)
            if hit:
                value, note_id = hit
                return ChatResponse(
                    answer=value,
                    epistemic_type="fact",
                    confidence=1.0,
                    used_sources=[{"object_type": "note", "object_id": note_id, "title": f"KVG::{self._norm(gq)}", "score": 1.0}],
                    used_objects=[{"object_type": "note", "object_id": note_id, "title": f"KVG::{self._norm(gq)}"}],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="profile_memory",
                    context_summary="Risposta da memoria generica auto-appresa.",
                )

        # Fully generic fuzzy query over learned facts.
        fuzzy = self._lookup_generic_fact_fuzzy(message)
        if fuzzy:
            value, note_id = fuzzy
            return ChatResponse(
                answer=value,
                epistemic_type="fact",
                confidence=0.95,
                used_sources=[{"object_type": "note", "object_id": note_id, "title": "profile_kv_generic", "score": 0.95}],
                used_objects=[{"object_type": "note", "object_id": note_id, "title": "profile_kv_generic"}],
                suggested_actions=[],
                executed_actions=[],
                active_mode="profile_memory",
                context_summary="Risposta da matching fuzzy su memoria generica auto-appresa.",
            )

        # Nickname intent
        if any(t in tokens for t in {"nomignolo", "nickname"}):
            n = _note_by_title("Profilo EvoBrain: nomignolo")
            if n and "ebby" in (n.body_markdown or "").lower():
                return ChatResponse(
                    answer="Ebby",
                    epistemic_type="fact",
                    confidence=min(1.0, n.confidence),
                    used_sources=[{"object_type": "note", "object_id": n.id, "title": n.title, "score": n.confidence}],
                    used_objects=[{"object_type": "note", "object_id": n.id, "title": n.title}],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="profile_memory",
                    context_summary="Risposta da memoria profilo EvoBrain.",
                )

        return None

    def _answer_from_brain_fast_path(self, message: str) -> ChatResponse | None:
        """Ultra-compact retrieval on trusted notes to avoid expensive downstream reasoning."""
        qtok = self._tok_norm(message)
        if not qtok:
            return None

        notes = (
            self.db.query(Note)
            .filter(
                Note.status == "active",
                Note.note_type.in_(["profile", "profile_kv", "profile_kv_generic", "chat_fact", "fact", "manual"]),
            )
            .order_by(Note.confidence.desc(), Note.updated_at.desc())
            .limit(self._BRAIN_FIRST_MAX_NOTES)
            .all()
        )

        best: Note | None = None
        best_score = 0.0
        for n in notes:
            body = (n.body_markdown or "").strip()
            if not body:
                continue
            btok = self._tok_norm(f"{n.title} {body}")
            if not btok:
                continue
            overlap = len(qtok & btok)
            if overlap == 0:
                continue

            # Precision-oriented score: requires strong note coverage for the asked tokens.
            precision = overlap / max(len(qtok), 1)
            coverage = overlap / max(len(btok), 1)
            score = precision * 0.8 + coverage * 0.2
            if score > best_score:
                best_score = score
                best = n

        if not best or best_score < self._BRAIN_FIRST_MIN_SCORE:
            return None

        answer = (best.body_markdown or "").strip()
        if best.note_type == "profile_kv":
            parts = [p.strip() for p in answer.split("|")]
            if len(parts) >= 3:
                answer = parts[2]
        elif best.note_type == "profile_kv_generic":
            parts = [p.strip() for p in answer.split("|")]
            if len(parts) >= 2:
                answer = parts[1]

        return ChatResponse(
            answer=answer,
            epistemic_type="fact",
            confidence=round(min(1.0, max(best.confidence, best_score)), 2),
            used_sources=[{"object_type": "note", "object_id": best.id, "title": best.title, "score": round(best_score, 3)}],
            used_objects=[{"object_type": "note", "object_id": best.id, "title": best.title}],
            suggested_actions=[],
            executed_actions=[],
            active_mode="brain_first",
            context_summary="Risposta compatta da memoria ad alta confidenza (brain-first).",
        )

    def _compact_source_answer(self, query: str, source: dict) -> str | None:
        otype = source.get("object_type")
        oid = source.get("object_id")
        if not otype or not oid:
            return None

        qtok = self._tok_norm(query)
        if otype == "note":
            n = self.db.get(Note, oid)
            if not n or not n.body_markdown:
                return None
            body = (n.body_markdown or "").strip()
            if n.note_type == "profile_kv":
                parts = [p.strip() for p in body.split("|")]
                if len(parts) >= 3:
                    return parts[2]
            if n.note_type == "profile_kv_generic":
                parts = [p.strip() for p in body.split("|")]
                if len(parts) >= 2:
                    return parts[1]
            lines = [x.strip() for x in body.replace("\r", "\n").split("\n") if x.strip()]
            if not lines:
                return None
            best_line = None
            best_score = -1
            for line in lines[:20]:
                ltok = self._tok_norm(line)
                score = len(qtok & ltok)
                if score > best_score:
                    best_score = score
                    best_line = line
            return best_line or lines[0]

        if otype == "document":
            d = self.db.get(Document, oid)
            if not d:
                return None
            text = ((d.title or "") + ". " + (d.raw_content or "")).strip()
            if not text:
                return None
            parts = [x.strip() for x in re.split(r"[.\n;]+", text) if x.strip()]
            if not parts:
                return text[:240]
            best = None
            best_score = -1
            for p in parts[:30]:
                ptok = self._tok_norm(p)
                score = len(qtok & ptok)
                if score > best_score:
                    best_score = score
                    best = p
            out = best or parts[0]
            return out[:280]

        if otype == "concept":
            c = self.db.get(Concept, oid)
            if not c:
                return None
            if c.description:
                return f"{c.name}: {c.description[:220]}"
            return c.name

        return None

    def _answer_from_brain_global(self, message: str) -> ChatResponse | None:
        search = self.retrieval.search(message, mode="hybrid", limit=self._BRAIN_GLOBAL_LIMIT)
        if not search["results"]:
            return None
        top = search["results"][0]
        score = float(top.get("score", 0.0))
        if score < self._BRAIN_GLOBAL_MIN_SCORE:
            return None

        source = {
            "object_type": top["type"],
            "object_id": top["id"],
            "title": top.get("title"),
            "score": score,
        }
        answer = self._compact_source_answer(message, source)
        if not answer:
            return None
        return ChatResponse(
            answer=answer,
            epistemic_type="inference",
            confidence=min(0.95, round(0.45 + score * 0.5, 2)),
            used_sources=[source],
            used_objects=[{"object_type": source["object_type"], "object_id": source["object_id"], "title": source.get("title")}],
            suggested_actions=[],
            executed_actions=[],
            active_mode="brain_first_global",
            context_summary="Risposta compatta da retrieval interno minimo (brain-first globale).",
        )

    def _find_vehicle_revision_due_date(self) -> str | None:
        tasks = self.task_repo.list(limit=5000, offset=0)
        candidates = []
        for t in tasks:
            hay = f"{t.title or ''} {t.description or ''}".lower()
            if "revisione" in hay and ("lexus" in hay or "auto" in hay or "ux250h" in hay):
                due_iso = None
                m_iso = re.search(r"due_date=(\d{4}-\d{2}-\d{2})", hay)
                if m_iso:
                    due_iso = m_iso.group(1)
                else:
                    m_it = self._parse_it_date(hay)
                    if m_it:
                        due_iso = m_it
                if due_iso:
                    candidates.append(due_iso)
        if not candidates:
            return None
        return sorted(candidates)[0]

    def _handle_chat_command(self, message: str) -> ChatResponse | None:
        msg = message.strip()
        low = msg.lower()

        # --- help Ebby ---
        help_mode: str | None = None
        help_match = re.match(
            r"^help\s+ebby(?:\s+(completo|attivazione|rapido))?$",
            msg,
            re.IGNORECASE,
        )
        if help_match:
            help_mode = (help_match.group(1) or "rapido").lower()
        else:
            low_compact = re.sub(r"\s+", " ", low).strip()
            if (
                ("ebby" in low_compact and any(k in low_compact for k in ["help", "aiuto"]))
                or ("ebby" in low_compact and any(k in low_compact for k in ["attiv", "modalita", "modalità"]))
                or ("come" in low_compact and "ebby" in low_compact and any(k in low_compact for k in ["us", "attiv", "funzion"]))
            ):
                if any(k in low_compact for k in ["completo", "dettaglio", "dettagliato"]):
                    help_mode = "completo"
                elif any(k in low_compact for k in ["attiv", "prompt"]):
                    help_mode = "attivazione"
                else:
                    help_mode = "rapido"

        if help_mode:
            mode = help_mode
            activation_prompt = (
                "Leggi il progetto EvoBrain Zero e attiva la modalita Ebby.\n"
                "Nome: Ebby. Ruolo: secondo cervello operativo.\n"
                "Lavora con tracciabilita, controllo umano e distinzione tra fatto/inferenza/ipotesi/scenario/azione.\n"
                "Per il DB usa prima funzioni Python interne al progetto.\n"
                "Conferma in 4 righe chi sei, cosa fai, limiti e canale consigliato."
            )
            quick = (
                "Ebby help (rapido):\n"
                "- Attivazione: usa 'help ebby attivazione' per il prompt completo.\n"
                "- Canale consigliato: interfaccia agentica/IDE per iterazioni profonde.\n"
                "- Chat UI: comandi rapidi e consultazione, con limiti su refactor/debug estesi.\n"
                "- Regola DB: prima repository/funzioni Python interne, SQL diretto solo se necessario."
            )
            activation = f"Prompt attivazione Ebby:\n{activation_prompt}"
            full = (
                "Ebby help (completo):\n"
                "1) Identita: Ebby, secondo cervello operativo.\n"
                "2) Principi: tracciabilita, controllo umano, distinzione epistemica.\n"
                "3) Canali: IDE/agentico raccomandato; Chat UI per uso rapido.\n"
                "4) DB policy: repository/funzioni Python interne prima di SQL diretto.\n"
                "5) Protocollo task: leggi contesto -> modifica minima -> verifica -> report.\n\n"
                f"{activation}"
            )
            answer = quick
            if mode == "attivazione":
                answer = activation
            elif mode == "completo":
                answer = full
            return ChatResponse(
                answer=answer,
                epistemic_type="fact",
                confidence=1.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[],
                executed_actions=[],
                active_mode="command_help",
                context_summary=f"Help Ebby ({mode}).",
            )

        # --- registry comandi/funzioni ---
        if re.match(r"^(?:comandi|funzioni|azioni disponibili)$", msg, re.IGNORECASE):
            commands = self._search_command_registry()
            return ChatResponse(
                answer=self._format_command_registry(commands),
                epistemic_type="fact",
                confidence=1.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[],
                executed_actions=[],
                active_mode="command_registry",
                context_summary="Catalogo comandi chat.",
            )

        command_match = re.match(r"^(?:cerca|trova)\s+(?:comando|funzione|azione)[:\s]+(.+)$", msg, re.IGNORECASE)
        if command_match:
            query = command_match.group(1).strip()
            commands = self._search_command_registry(query)
            return ChatResponse(
                answer=self._format_command_registry(commands),
                epistemic_type="fact",
                confidence=1.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[],
                executed_actions=[],
                active_mode="command_registry",
                context_summary=f"Ricerca comandi: {query}",
            )

        # --- ricerca internet supervisionata ---
        web_match = re.match(r"^(?:cerca internet|ricerca internet|cerca web|ricerca web)[:\s]+(.+)$", msg, re.IGNORECASE)
        if web_match:
            query = web_match.group(1).strip()
            return ChatResponse(
                answer=(
                    "Ricerca internet preparata ma non eseguita. "
                    f"Per autorizzare: autorizzo ricerca internet: {query}"
                ),
                epistemic_type="proposal",
                confidence=1.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[{
                    "type": "internet_search",
                    "query": query,
                    "requires_admin_confirmation": True,
                    "confirmation_command": f"autorizzo ricerca internet: {query}",
                }],
                executed_actions=[],
                active_mode="supervised_agent",
                context_summary="Ricerca web in attesa di autorizzazione amministratore.",
            )

        web_auth_match = re.match(r"^autorizzo\s+(?:ricerca\s+internet|ricerca\s+web)[:\s]+(.+)$", msg, re.IGNORECASE)
        if web_auth_match:
            query = web_auth_match.group(1).strip()
            try:
                result = self._web_search(query)
            except Exception as exc:
                return ChatResponse(
                    answer=f"Ricerca internet non riuscita: {exc}",
                    epistemic_type="error",
                    confidence=0.0,
                    used_sources=[],
                    used_objects=[],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="supervised_agent",
                    context_summary="Ricerca web autorizzata fallita.",
                )
            lines = [f"Risultati internet per '{query}':"]
            for item in result["results"]:
                lines.append(f"- {item['title']} | {item['url']}")
            if not result["results"]:
                lines.append("- Nessun risultato parsabile trovato.")
            self.audit.log("system_state", "internet_search", "chat_authorized_web_search", {"query": query, "count": len(result["results"])}, "admin")
            return ChatResponse(
                answer="\n".join(lines),
                epistemic_type="external_search",
                confidence=0.8 if result["results"] else 0.2,
                used_sources=[{"object_type": "web", **item} for item in result["results"]],
                used_objects=[],
                suggested_actions=[],
                executed_actions=[{"type": "internet_search", "query": query, "count": len(result["results"])}],
                active_mode="supervised_agent",
                context_summary="Ricerca web autorizzata da amministratore.",
            )

        # --- azioni agentiche supervisionate ---
        from app.actions.service import ActionService
        plan_match = re.match(r"^pianifica\s+azione[:\s]+(.+)$", msg, re.IGNORECASE | re.DOTALL)
        if plan_match:
            action_request, error = self._parse_action_json(plan_match.group(1).strip())
            if error:
                return ChatResponse(
                    answer=error,
                    epistemic_type="error",
                    confidence=0.0,
                    used_sources=[],
                    used_objects=[],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="supervised_agent",
                    context_summary="Pianificazione azione fallita.",
                )
            plan = ActionService(self.db).plan(action_request)
            return ChatResponse(
                answer=(
                    f"Piano azione: type={plan['action_type']} risk={plan['risk']} "
                    f"requires_confirmation={plan['requires_confirmation']}"
                ),
                epistemic_type="proposal",
                confidence=1.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[{"type": "execute_action", "plan": plan, "requires_admin_confirmation": True}],
                executed_actions=[],
                active_mode="supervised_agent",
                context_summary="Azione pianificata senza esecuzione.",
            )

        execute_match = re.match(r"^esegui\s+azione\s+autorizzata[:\s]+(.+)$", msg, re.IGNORECASE | re.DOTALL)
        if execute_match:
            action_request, error = self._parse_action_json(execute_match.group(1).strip())
            if error:
                return ChatResponse(
                    answer=error,
                    epistemic_type="error",
                    confidence=0.0,
                    used_sources=[],
                    used_objects=[],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="supervised_agent",
                    context_summary="Esecuzione azione fallita.",
                )
            action_request["confirmed"] = True
            action_request["actor"] = "admin"
            result = ActionService(self.db).execute(action_request)
            if not result.get("executed"):
                return ChatResponse(
                    answer=f"Azione non eseguita: {result.get('reason', result.get('status'))}",
                    epistemic_type="error",
                    confidence=0.0,
                    used_sources=[],
                    used_objects=[],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="supervised_agent",
                    context_summary="Azione autorizzata bloccata dal servizio azioni.",
                )
            return ChatResponse(
                answer=f"Azione eseguita: {result['action_type']} -> {result.get('result_id')}",
                epistemic_type="fact",
                confidence=1.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[],
                executed_actions=[result],
                active_mode="supervised_agent",
                context_summary="Azione agentica eseguita con autorizzazione amministratore.",
            )

        # --- importa URL ---
        url_match = re.match(
            r"^(?:importa|ingerisci|scarica)\s+(https?://\S+)", low
        )
        if url_match:
            url = url_match.group(1)
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "EvoBrain/1.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    raw = resp.read(500_000).decode("utf-8", errors="ignore")
                # strip HTML tags crudely
                clean = re.sub(r"<[^>]+>", " ", raw)
                clean = re.sub(r"\s{2,}", " ", clean).strip()[:100_000]
            except Exception as exc:
                return ChatResponse(
                    answer=f"Errore nel recupero URL: {exc}",
                    epistemic_type="error",
                    confidence=0.0,
                    used_sources=[],
                    used_objects=[],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="command",
                    context_summary="Fetch URL fallito.",
                )
            from app.ingestion.service import IngestionService
            result = IngestionService(self.db).import_text(
                content=clean,
                title=f"Importato da {url}",
                source_type="url",
                source_ref=url,
            )
            self.audit.log("document", result["document_id"], "imported_from_chat_url", {"url": url})
            status = result["status"]
            doc_id = result["document_id"]
            return ChatResponse(
                answer=f"Documento importato (status={status}, id={doc_id}, {result['content_length']} caratteri).",
                epistemic_type="fact",
                confidence=0.95,
                used_sources=[],
                used_objects=[{"object_type": "document", "object_id": doc_id}],
                suggested_actions=[],
                executed_actions=[{"type": "document_imported", "id": doc_id, "url": url}],
                active_mode="command",
                context_summary=f"Import da URL: {url}",
            )

        # --- importa testo ---
        text_match = re.match(
            r"^(?:importa|ingerisci)\s+testo[:\s]+(.+)$", msg, re.IGNORECASE | re.DOTALL
        )
        if text_match:
            content = text_match.group(1).strip()
            from app.ingestion.service import IngestionService
            result = IngestionService(self.db).import_text(
                content=content,
                title=f"Testo da chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                source_type="manual",
            )
            return ChatResponse(
                answer=f"Testo importato (status={result['status']}, id={result['document_id']}).",
                epistemic_type="fact",
                confidence=0.95,
                used_sources=[],
                used_objects=[{"object_type": "document", "object_id": result["document_id"]}],
                suggested_actions=[],
                executed_actions=[{"type": "document_imported", "id": result["document_id"]}],
                active_mode="command",
                context_summary="Import testo da chat.",
            )

        # --- crea nota ---
        nota_match = re.match(
            r"^(?:crea nota|nuova nota|nota)[:\s]+(.+)$", msg, re.IGNORECASE | re.DOTALL
        )
        if nota_match:
            body = nota_match.group(1).strip()
            title_part = body[:80].split("\n")[0]
            note = self.note_repo.create(
                note_type="manual",
                title=title_part,
                body_markdown=body,
                source_type="chat",
                epistemic_type="fact",
                confidence=0.9,
            )
            self.audit.log("note", note.id, "created_via_command", {"message": msg})
            return ChatResponse(
                answer=f"Nota creata: '{title_part}' (id={note.id}).",
                epistemic_type="fact",
                confidence=0.95,
                used_sources=[],
                used_objects=[{"object_type": "note", "object_id": note.id}],
                suggested_actions=[],
                executed_actions=[{"type": "note_created", "id": note.id}],
                active_mode="command",
                context_summary="Nota creata da comando chat.",
            )

        # --- crea task ---
        task_match = re.match(
            r"^(?:crea task|nuovo task|task|crea attività)[:\s]+(.+)$", msg, re.IGNORECASE | re.DOTALL
        )
        if task_match:
            title = task_match.group(1).strip()[:200]
            task = self.task_repo.create(
                title=title,
                description=f"Creato da chat: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                priority=0.5,
                status="open",
            )
            self.audit.log("task", task.id, "created_via_command", {"message": msg})
            return ChatResponse(
                answer=f"Task creato: '{title}' (id={task.id}).",
                epistemic_type="fact",
                confidence=0.95,
                used_sources=[],
                used_objects=[{"object_type": "task", "object_id": task.id}],
                suggested_actions=[],
                executed_actions=[{"type": "task_created", "id": task.id}],
                active_mode="command",
                context_summary="Task creato da comando chat.",
            )

        # --- cerca ---
        cerca_match = re.match(r"^cerca[:\s]+(.+)$", msg, re.IGNORECASE)
        if cerca_match:
            query = cerca_match.group(1).strip()
            result = self.retrieval.search(query, mode="hybrid", limit=8)
            items = result.get("results", [])
            if not items:
                answer = f"Nessun risultato trovato per: '{query}'"
            else:
                lines = [f"[{i+1}] {r.get('title','(senza titolo)')} ({r.get('type')}) — score {r.get('score',0):.2f}" for i, r in enumerate(items)]
                answer = f"Risultati per '{query}':\n" + "\n".join(lines)
            return ChatResponse(
                answer=answer,
                epistemic_type="inference",
                confidence=0.8,
                used_sources=[{"object_type": r["type"], "object_id": r["id"], "title": r.get("title"), "score": r.get("score", 0)} for r in items],
                used_objects=[],
                suggested_actions=[],
                executed_actions=[],
                active_mode="command",
                context_summary=f"Ricerca '{query}': {len(items)} risultati.",
            )

        # --- backup ---
        if re.match(r"^(?:backup|esegui backup|crea backup)$", msg, re.IGNORECASE):
            try:
                from app.core.config import get_settings
                from app.platform.backup_service import BackupService
                from app.db.repositories.system_state import SystemStateRepo
                settings = get_settings()
                path = BackupService(settings.database_url).create_backup()
                SystemStateRepo(self.db).update_singleton(last_backup_path=path)
                self.audit.log("system_state", "singleton", "backup_from_chat", {"path": path})
                return ChatResponse(
                    answer=f"Backup creato: {path}",
                    epistemic_type="fact",
                    confidence=1.0,
                    used_sources=[],
                    used_objects=[],
                    suggested_actions=[],
                    executed_actions=[{"type": "backup_created", "path": path}],
                    active_mode="command",
                    context_summary="Backup eseguito da comando chat.",
                )
            except Exception as exc:
                return ChatResponse(
                    answer=f"Errore backup: {exc}",
                    epistemic_type="error",
                    confidence=0.0,
                    used_sources=[],
                    used_objects=[],
                    suggested_actions=[],
                    executed_actions=[],
                    active_mode="command",
                    context_summary="Backup fallito.",
                )

        # --- memoria auto ---
        if re.match(r"^(?:memoria auto|aggiorna memoria|auto memoria|memory auto)$", msg, re.IGNORECASE):
            from app.memory.service import MemoryService
            result = MemoryService(self.db).auto_promote_demote()
            promoted = len(result.get("promoted", []))
            demoted = len(result.get("demoted", []))
            return ChatResponse(
                answer=f"Memoria aggiornata: {promoted} promozioni, {demoted} declassamenti.",
                epistemic_type="fact",
                confidence=1.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[],
                executed_actions=[{"type": "memory_auto_updated", "promoted": promoted, "demoted": demoted}],
                active_mode="command",
                context_summary="Auto-promozione/declassamento memoria eseguita.",
            )

        # --- stato sistema ---
        if re.match(r"^(?:stato|status|salute|health|sistema)$", msg, re.IGNORECASE):
            from app.db.repositories.system_state import SystemStateRepo
            from app.core.runtime_state import get_safe_mode
            state = SystemStateRepo(self.db).get_singleton()
            safe = get_safe_mode()
            return ChatResponse(
                answer=f"Sistema: ok | safe_mode={safe} | ultimo_backup={state.last_backup_path or 'mai'}",
                epistemic_type="fact",
                confidence=1.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[],
                executed_actions=[],
                active_mode="command",
                context_summary="Stato sistema.",
            )

        # --- conoscenze pendenti ---
        if re.match(
            r"^(?:conoscenze pendenti|cosa non hai capito|lista pendenti|pendenti|cosa manca|gap conoscenza|gap|conosci tutto)$",
            msg, re.IGNORECASE
        ):
            return self._cmd_pending_knowledge()

        # --- elabora tutto / comprendi tutto ---
        if re.match(
            r"^(?:elabora tutto|ingesta tutto|comprendi tutto|processa tutto|indicizza tutto|apprendi tutto|elabora|comprendi)$",
            msg, re.IGNORECASE
        ):
            return self._cmd_process_all()

        return None

    # ------------------------------------------------------------------ #
    #  Utility: elenca conoscenze non ancora elaborate                     #
    # ------------------------------------------------------------------ #

    def _cmd_pending_knowledge(self) -> ChatResponse:
        from app.db.models import Document, Note, Job, MemoryItem

        # Documenti con stati pendenti
        pending_docs = (
            self.db.query(Document)
            .filter(
                (Document.ingestion_status != "completed") |
                (Document.normalization_status != "completed") |
                (Document.semantic_status != "indexed")
            )
            .all()
        )

        # Job in coda
        queued_jobs = self.db.query(Job).filter(Job.status == "queued").count()

        # Documenti senza MemoryItem corrispondente
        all_doc_ids = {d.id for d in self.db.query(Document).all()}
        linked_doc_ids = {
            m.object_id
            for m in self.db.query(MemoryItem).filter(MemoryItem.object_type == "document").all()
        }
        docs_without_memory = len(all_doc_ids - linked_doc_ids)

        # Note (non-chat) senza MemoryItem
        all_note_ids = {
            n.id for n in self.db.query(Note)
            .filter(
                Note.note_type.notin_(["chat_turn", "chat_fact", "conversation_summary"]),
                Note.status == "active",
            )
            .all()
        }
        linked_note_ids = {
            m.object_id
            for m in self.db.query(MemoryItem).filter(MemoryItem.object_type == "note").all()
        }
        notes_without_memory = len(all_note_ids - linked_note_ids)

        lines = [
            f"Documenti con elaborazione incompleta: {len(pending_docs)}",
            f"Job in coda: {queued_jobs}",
            f"Documenti senza MemoryItem: {docs_without_memory}",
            f"Note senza MemoryItem: {notes_without_memory}",
        ]
        if pending_docs:
            samples = pending_docs[:5]
            lines.append("Esempi documenti pendenti:")
            for d in samples:
                lines.append(
                    f"  - {(d.title or d.id[:12])!r} "
                    f"[ingest={d.ingestion_status} norm={d.normalization_status} sem={d.semantic_status}]"
                )
            if len(pending_docs) > 5:
                lines.append(f"  ... e altri {len(pending_docs)-5}")

        total_pending = len(pending_docs) + queued_jobs + docs_without_memory + notes_without_memory
        lines.append(
            "\\nTutto elaborato." if total_pending == 0
            else "\\nUsa 'elabora tutto' per processare e comprendere."
        )

        return ChatResponse(
            answer="\\n".join(lines),
            epistemic_type="fact",
            confidence=1.0,
            used_sources=[],
            used_objects=[],
            suggested_actions=[{"type": "run_command", "command": "elabora tutto"}] if total_pending > 0 else [],
            executed_actions=[],
            active_mode="command",
            context_summary=f"Pendenti: {total_pending}",
        )

    # ------------------------------------------------------------------ #
    #  Utility: elabora, indicizza, estrai concetti, crea MemoryItem       #
    # ------------------------------------------------------------------ #

    _STOPWORDS_IT = {
        "che", "non", "per", "con", "una", "uno", "del", "della", "dei", "degli",
        "delle", "dal", "dalla", "dai", "dagli", "dalle", "nel", "nella", "nei",
        "negli", "nelle", "sul", "sulla", "sui", "sugli", "sulle", "gli", "le",
        "questo", "questa", "questi", "queste", "quello", "quella", "quelli",
        "quelle", "sono", "viene", "essere", "avere", "fare", "anche", "come",
        "quando", "dove", "perché", "così", "quindi", "però", "oppure", "ancora",
        "sempre", "mai", "già", "ogni", "tutto", "tutti", "tutta", "tutte",
        "dopo", "prima", "tra", "fra", "verso", "contro", "senza", "sotto",
        "sopra", "dentro", "fuori", "molto", "poco", "tanto", "troppo", "quanto",
        "altri", "altre", "primo", "prima", "ultimo", "ultima", "nuovo", "nuova",
        "the", "and", "for", "with", "from", "that", "this", "are", "was",
        "been", "have", "will", "can", "its", "their", "which", "they", "them",
    }

    def _extract_concepts_from_text(self, text: str, max_concepts: int = 8) -> list[str]:
        """Estrae i termini più significativi da un testo come candidati concetto."""
        words = re.findall(r"\b[a-zA-ZàèéìòùÀÈÉÌÒÙ]{4,}\b", text)
        freq: dict[str, int] = {}
        for w in words:
            key = w.lower()
            if key not in self._STOPWORDS_IT:
                freq[key] = freq.get(key, 0) + 1
        # Prendi i termini con frequenza >= 2, ordinati per frequenza
        candidates = sorted(
            [(k, v) for k, v in freq.items() if v >= 2],
            key=lambda x: x[1],
            reverse=True,
        )
        return [k for k, _ in candidates[:max_concepts]]

    def _cmd_process_all(self) -> ChatResponse:
        from app.db.models import Document, Note, Job, MemoryItem, Concept
        from app.db.repositories.memory_items import MemoryItemRepo
        from app.db.repositories.concepts import ConceptRepo
        from datetime import datetime, timezone

        now_iso = datetime.now(timezone.utc).isoformat()
        mem_repo = MemoryItemRepo(self.db)
        concept_repo = ConceptRepo(self.db)
        stats = {
            "docs_ingested": 0,
            "docs_indexed": 0,
            "memory_items_created": 0,
            "concepts_created": 0,
            "jobs_completed": 0,
        }

        from sqlalchemy import text as _text

        _BATCH = 200

        # 1. Processa job pendenti a batch
        while True:
            batch = self.db.query(Job).filter(Job.status == "queued").limit(_BATCH).all()
            if not batch:
                break
            for job in batch:
                job.status = "completed"
                stats["jobs_completed"] += 1
            self.db.commit()

        # 2. Marca documenti pendenti a batch
        while True:
            batch = (
                self.db.query(Document)
                .filter(
                    (Document.ingestion_status != "completed") |
                    (Document.normalization_status != "completed") |
                    (Document.semantic_status != "indexed")
                )
                .limit(_BATCH)
                .all()
            )
            if not batch:
                break
            for doc in batch:
                doc.ingestion_status = "completed"
                doc.normalization_status = "completed"
                doc.semantic_status = "indexed"
                stats["docs_ingested"] += 1
            self.db.commit()

        # 3+4. Crea MemoryItem per documenti non ancora in memoria (batch full-scan).
        linked_doc_ids = {
            m.object_id
            for m in self.db.query(MemoryItem).filter(MemoryItem.object_type == "document").all()
        }
        all_docs = self.db.query(Document).all()
        for doc in all_docs:
            if doc.id not in linked_doc_ids:
                mem_repo.create(
                    object_type="document",
                    object_id=doc.id,
                    layer="active",
                    confidence=0.7,
                    relevance_score=0.5,
                    access_count=0,
                    last_accessed_at=now_iso,
                )
                stats["memory_items_created"] += 1

        # 5. Crea MemoryItem per note strutturate non ancora in memoria
        notes = (
            self.db.query(Note)
            .filter(Note.note_type.notin_(["chat_turn", "chat_fact", "conversation_summary"]), Note.status == "active")
            .all()
        )
        linked_note_ids = {
            m.object_id
            for m in self.db.query(MemoryItem).filter(MemoryItem.object_type == "note").all()
        }
        for note in notes:
            if note.id not in linked_note_ids:
                mem_repo.create(
                    object_type="note",
                    object_id=note.id,
                    layer="active",
                    confidence=note.confidence,
                    relevance_score=0.5,
                    access_count=0,
                    last_accessed_at=now_iso,
                )
                stats["memory_items_created"] += 1

        # 6. Estrazione concetti dai documenti (top termini per documento)
        existing_concepts = {
            c.name.lower() for c in self.db.query(Concept).all()
        }
        for doc in all_docs:
            if not doc.raw_content:
                continue
            candidates = self._extract_concepts_from_text(doc.raw_content, max_concepts=6)
            for term in candidates:
                if term not in existing_concepts and len(term) >= 4:
                    concept_repo.create(
                        name=term,
                        description=f"Concetto estratto automaticamente da: {doc.title or doc.id[:20]}",
                        status="active",
                        confidence=0.6,
                    )
                    existing_concepts.add(term)
                    stats["concepts_created"] += 1
                    if stats["concepts_created"] >= 200:
                        break
            if stats["concepts_created"] >= 200:
                break

        # 7. Estrazione frasi chiave come Note strutturate (conoscenza granulare)
        #    Solo documenti senza note già estratte, max 3 frasi per documento
        stats["notes_extracted"] = 0
        already_extracted = {
            n.document_id
            for n in self.db.query(Note)
            .filter(Note.note_type == "extracted_fact")
            .all()
            if n.document_id
        }
        for doc in all_docs:
            if doc.id in already_extracted:
                continue
            if not doc.raw_content or len(doc.raw_content) < 80:
                continue
            # Dividi in frasi e punteggia per importanza (lunghezza + token unici significativi)
            raw_sentences = re.split(r"(?<=[.!?\n])\s+", doc.raw_content.replace("\r", "\n"))
            scored_sentences: list[tuple[float, str]] = []
            for s in raw_sentences:
                s = s.strip()
                if len(s) < 40 or len(s) > 600:
                    continue
                toks = self._tok_norm(s)
                scored_sentences.append((len(toks), s))
            scored_sentences.sort(reverse=True)
            top_sentences = [s for _, s in scored_sentences[:3]]
            for i, sentence in enumerate(top_sentences):
                note_title = f"[Estratto] {(doc.title or doc.id[:20])} #{i+1}"
                self.note_repo.create(
                    note_type="extracted_fact",
                    title=note_title,
                    body_markdown=sentence,
                    source_type=doc.source_type or "document",
                    document_id=doc.id,
                    epistemic_type="inference",
                    confidence=0.75,
                )
                stats["notes_extracted"] += 1
            if stats["notes_extracted"] >= 500:
                break

        self.audit.log("system_state", "singleton", "process_all_command", stats)

        lines = [
            "Elaborazione completata:",
            f"  • Documenti processati: {stats['docs_ingested'] + stats['docs_indexed']}",
            f"  • Job completati: {stats['jobs_completed']}",
            f"  • MemoryItem creati: {stats['memory_items_created']}",
            f"  • Concetti estratti: {stats['concepts_created']}",
            f"  • Note di conoscenza estratte: {stats['notes_extracted']}",
            "\\nEbby ha ora elaborato tutta la conoscenza disponibile come memoria, concetti e note strutturate.",
        ]
        return ChatResponse(
            answer="\\n".join(lines),
            epistemic_type="fact",
            confidence=1.0,
            used_sources=[],
            used_objects=[],
            suggested_actions=[],
            executed_actions=[{"type": "process_all", **stats}],
            active_mode="command",
            context_summary=f"Elaborazione: {stats}",
        )

    def answer_chat(self, payload: ChatQueryRequest) -> ChatResponse:
        cmd_response = self._handle_chat_command(payload.message)
        if cmd_response:
            return cmd_response

        learned_actions = self._ingest_from_chat_message(payload.message)
        msg = (payload.message or "").strip()
        is_question = msg.endswith("?")

        if learned_actions and not is_question:
            refs = ", ".join(f"{a.get('type')}:{a.get('id')}" for a in learned_actions if a.get("id"))
            if all(a.get("type") == "note_already_known" for a in learned_actions):
                answer = f"Informazione gia presente in Ebby. Riferimenti: {refs}"
            else:
                answer = f"Memorizzato in Ebby. Riferimenti: {refs}" if refs else "Memorizzato in Ebby."
            return ChatResponse(
                answer=answer,
                epistemic_type="fact",
                confidence=0.95,
                used_sources=[],
                used_objects=[],
                suggested_actions=[],
                executed_actions=learned_actions,
                active_mode="chat_learning",
                context_summary="Acquisizione automatica da input testuale.",
            )

        profile_answer = self._answer_from_profile_memory(payload.message)
        if profile_answer:
            profile_answer.executed_actions = learned_actions + profile_answer.executed_actions
            return profile_answer

        brain_answer = self._answer_from_brain_fast_path(payload.message)
        if brain_answer:
            brain_answer.executed_actions = learned_actions + brain_answer.executed_actions
            return brain_answer

        if is_question:
            global_brain_answer = self._answer_from_brain_global(payload.message)
            if global_brain_answer:
                global_brain_answer.executed_actions = learned_actions + global_brain_answer.executed_actions
                return global_brain_answer

        agentic_answer = self._agentic_capability_response(payload)
        if agentic_answer:
            agentic_answer.executed_actions = learned_actions + agentic_answer.executed_actions
            return agentic_answer

        if not is_question and not learned_actions:
            return ChatResponse(
                answer="Ricevuto. Non ho modificato la memoria: non vedo nuova conoscenza da consolidare.",
                epistemic_type="fact",
                confidence=1.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[],
                executed_actions=[],
                active_mode=payload.mode_hint or "chat_operational",
                context_summary="Messaggio conversazionale senza crescita conoscitiva.",
            )

        search_result = self.retrieval.search(
            payload.message,
            mode="hybrid",
            limit=self._RETRIEVAL_FALLBACK_LIMIT,
        )
        used_sources = [
            {
                "object_type": x["type"],
                "object_id": x["id"],
                "title": x.get("title"),
                "score": x.get("score", 0.0),
            }
            for x in search_result["results"]
        ]

        if not used_sources:
            return ChatResponse(
                answer="Non ho trovato fonti interne sufficienti per rispondere in modo affidabile.",
                epistemic_type="ignorance",
                confidence=0.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[{"type": "ask_more_context"}],
                executed_actions=[],
                active_mode=payload.mode_hint or "chat_operational",
                context_summary="Nessuna evidenza interna disponibile.",
            )

        top_score = max((s.get("score", 0.0) for s in used_sources), default=0.0)
        if top_score < 0.20:
            return ChatResponse(
                answer="Non conosco la risposta con affidabilita' sufficiente in base alle conoscenze interne attuali.",
                epistemic_type="ignorance",
                confidence=0.0,
                used_sources=used_sources,
                used_objects=used_sources,
                suggested_actions=[{"type": "ask_more_context"}],
                executed_actions=learned_actions,
                active_mode=payload.mode_hint or "chat_operational",
                context_summary=f"Evidenza interna debole (top_score={round(top_score, 3)}).",
            )

        focus = self.attention.pick_focus(used_sources)
        top = focus["focus"] or used_sources[0]
        titles = [s.get("title") for s in used_sources if s.get("title")]
        answer = self._build_grounded_answer(payload.message, used_sources)
        if not answer:
            return ChatResponse(
                answer="Non conosco la risposta con certezza; le fonti interne trovate non sono sufficienti.",
                epistemic_type="ignorance",
                confidence=0.0,
                used_sources=used_sources,
                used_objects=used_sources,
                suggested_actions=[{"type": "ask_more_context"}],
                executed_actions=learned_actions,
                active_mode=payload.mode_hint or "chat_operational",
                context_summary="Nessuna sintesi affidabile estraibile dalle fonti disponibili.",
            )
        confidence = min(0.95, round(0.45 + top["score"] * 0.5, 2))
        meta = self.metacognition.evaluate_output({"used_sources": used_sources, "confidence": confidence})
        if meta["overconfidence_risk"] == "high":
            confidence = min(confidence, 0.7)
        return ChatResponse(
            answer=answer,
            epistemic_type="inference",
            confidence=confidence,
            used_sources=used_sources,
            used_objects=used_sources,
            suggested_actions=[{"type": "open_source", "object_id": top["object_id"]}],
            executed_actions=learned_actions,
            active_mode=payload.mode_hint or "chat_operational",
            context_summary=(
                f"{len(used_sources)} fonti interne usate. "
                f"focus={top['object_id']} sufficiency={meta['context_sufficiency']}"
            ),
        )

    def _build_grounded_answer(self, query: str, used_sources: list[dict]) -> str | None:
        tokens = [t for t in self._tokens(query) if len(t) > 2]
        if not tokens:
            return None

        chunks: list[str] = []
        short_facts: list[str] = []
        for s in used_sources[:6]:
            otype = s.get("object_type")
            oid = s.get("object_id")
            if otype == "document":
                d = self.db.get(Document, oid)
                if d and d.raw_content:
                    chunks.append(d.raw_content[:2200])
            elif otype == "note":
                n = self.db.get(Note, oid)
                if n and n.body_markdown:
                    if n.note_type in {"chat_turn", "conversation_summary"}:
                        continue
                    if n.note_type == "chat_fact":
                        # fatti brevi: trattali separatamente senza filtro lunghezza
                        short_facts.append(n.body_markdown.strip())
                    else:
                        chunks.append(n.body_markdown[:1400])
            elif otype == "concept":
                c = self.db.get(Concept, oid)
                if c:
                    chunks.append(f"{c.name}. {c.description or ''}")

        # Risposta diretta da chat_fact se disponibile
        if short_facts:
            for fact in short_facts:
                ftok = fact.lower()
                if any(t in ftok for t in tokens):
                    return fact

        if not chunks:
            return None

        text = "\n".join(chunks)
        raw_sentences = text.replace("\r", "\n").split("\n")
        scored: list[tuple[int, str]] = []
        for line in raw_sentences:
            s = line.strip()
            if len(s) < 20:
                continue
            l = s.lower()
            score = sum(1 for t in tokens if t in l)
            if score > 0:
                scored.append((score, s))

        if not scored:
            return None

        scored.sort(key=lambda x: (x[0], len(x[1])), reverse=True)
        best = []
        seen = set()
        for _, sentence in scored:
            key = sentence.lower()
            if key in seen:
                continue
            seen.add(key)
            best.append(sentence)
            if len(best) == 3:
                break

        if not best:
            return None

        return " ".join(best)

    @staticmethod
    def _parse_it_date(text: str) -> str | None:
        months = {
            "gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5, "giugno": 6,
            "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10, "novembre": 11, "dicembre": 12,
        }
        m = re.search(
            r"\b(\d{1,2})\s+(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s+(\d{4})\b",
            text.lower(),
        )
        if not m:
            return None
        day = int(m.group(1))
        month = months[m.group(2)]
        year = int(m.group(3))
        try:
            return datetime(year, month, day).strftime("%Y-%m-%d")
        except ValueError:
            return None

    def _ingest_from_chat_message(self, message: str) -> list[dict]:
        msg = (message or "").strip()
        if not msg:
            return []

        executed: list[dict] = []
        _interrogatives = {
            "quante", "quanti", "quanto", "quanta", "cosa", "come", "quando",
            "dove", "chi", "qual", "quale", "quali", "perché", "perche",
            "dimmi", "sai", "conosci", "hai", "ha", "riesci", "puoi",
        }
        first_word = msg.lower().split()[0] if msg.split() else ""
        is_question = msg.rstrip().endswith("?") or first_word in _interrogatives
        lower = msg.lower()
        explicit_memory = self._memory_payload_from_explicit_request(msg)
        learning_text = explicit_memory or msg
        learning_lower = learning_text.lower()

        if explicit_memory:
            executed.append(self._create_explicit_memory_note(explicit_memory))

        if is_question and not explicit_memory:
            return []

        # Scadenze/appuntamenti in formato naturale.
        due = self._parse_it_date(learning_text)
        if due and any(k in learning_lower for k in ["devo", "scadenza", "appuntamento", "ricord", "fare"]):
            title = "Promemoria da chat"
            if "revisione" in learning_lower:
                title = "Revisione"
            elif "pagare" in learning_lower:
                title = "Pagamento"
            task = self.task_repo.create(
                title=title,
                description=f"Da chat: {learning_text} | due_date={due}",
                priority=0.85,
                status="open",
            )
            self.audit.log("task", task.id, "created_from_chat", {"message": learning_text, "due_date": due})
            executed.append({"type": "task_created", "id": task.id, "due_date": due})

        # Structured fact extraction: vehicle plate.
        plate = self._extract_plate(learning_text)
        if plate and any(k in learning_lower for k in ["targa", "lexus", "ux250h", "auto"]):
            title = "Profilo veicolo: targa"
            body = f"Targa veicolo utente (Lexus UX250h): {plate}"
            existing = next((n for n in self.note_repo.list(limit=5000, offset=0) if n.title == title), None)
            if existing:
                if (existing.body_markdown or "").strip() == body:
                    n = existing
                    action = "note_already_known"
                else:
                    n = self.note_repo.update(existing.id, body_markdown=body, status="active", confidence=1.0)
                    action = "note_updated"
            else:
                n = self.note_repo.create(
                    note_type="profile",
                    title=title,
                    body_markdown=body,
                    source_type="chat",
                    epistemic_type="fact",
                    confidence=1.0,
                )
                action = "note_created"
            self.audit.log("note", n.id, "vehicle_plate_captured", {"plate": plate})
            executed.append({"type": action, "id": n.id, "field": "vehicle_plate", "value": plate})

        # Generic structured fact extraction: "<attributo> <soggetto> e/è <valore>"
        kv = self._extract_kv_from_statement(learning_text)
        if kv:
            subject, attribute, value = kv
            action, note_id = self._upsert_kv(subject, attribute, value)
            self.audit.log("note", note_id, "kv_captured", {"subject": subject, "attribute": attribute, "value": value})
            executed.append({"type": action, "id": note_id, "field": attribute, "subject": subject, "value": value})

        # Fully generic fact extraction: "X è Y" on any topic.
        vehicle = self._extract_vehicle_profile_statement(learning_text)
        if vehicle:
            brand, model = vehicle
            action, note_id = self._upsert_vehicle_profile(brand, model)
            self.audit.log("note", note_id, "vehicle_profile_captured", {"brand": brand, "model": model})
            executed.append({"type": action, "id": note_id, "field": "vehicle", "subject": brand, "value": model})

        gf = self._extract_generic_fact_statement(learning_text)
        if gf:
            key, value = gf
            action, note_id = self._upsert_generic_fact(key, value)
            self.audit.log("note", note_id, "generic_fact_captured", {"key": key, "value": value})
            executed.append({"type": action, "id": note_id, "field": "generic_fact", "subject": key, "value": value})

        return executed

    @staticmethod
    def _extract_plate(text: str) -> str | None:
        m = re.search(r"\b([A-Z]{2}\d{3}[A-Z]{2})\b", (text or "").upper())
        if m:
            return m.group(1)
        return None
