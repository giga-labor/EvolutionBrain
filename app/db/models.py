from sqlalchemy import String, Text, Float, Integer, BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, IdMixin, TimestampMixin


class Document(Base, IdMixin, TimestampMixin):
    __tablename__ = "documents"

    source_type: Mapped[str] = mapped_column(String, nullable=False)
    source_ref: Mapped[str | None] = mapped_column(String, nullable=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    content_hash: Mapped[str] = mapped_column(String, nullable=False, index=True)
    raw_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    ingestion_status: Mapped[str] = mapped_column(String, nullable=False, default="raw_pending")
    normalization_status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    semantic_status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    validation_status: Mapped[str] = mapped_column(String, nullable=False, default="unvalidated")


class Note(Base, IdMixin, TimestampMixin):
    __tablename__ = "notes"

    document_id: Mapped[str | None] = mapped_column(ForeignKey("documents.id"), nullable=True)
    note_type: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")
    epistemic_type: Mapped[str] = mapped_column(String, nullable=False, default="fact")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)


class Project(Base, IdMixin, TimestampMixin):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    project_type: Mapped[str] = mapped_column(String, nullable=False, default="general")
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")


class Job(Base, IdMixin, TimestampMixin):
    __tablename__ = "jobs"

    job_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="queued")
    priority: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class AuditEntry(Base, IdMixin, TimestampMixin):
    __tablename__ = "audit_entries"

    entity_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    actor: Mapped[str | None] = mapped_column(String, nullable=True)
    payload: Mapped[str | None] = mapped_column(Text, nullable=True)


class Concept(Base, IdMixin, TimestampMixin):
    __tablename__ = "concepts"

    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.7)


class Relation(Base, IdMixin, TimestampMixin):
    __tablename__ = "relations"

    source_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    target_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    relation_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.7)
    evidence: Mapped[str | None] = mapped_column(Text, nullable=True)


class MemoryItem(Base, IdMixin, TimestampMixin):
    __tablename__ = "memory_items"

    object_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    object_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    layer: Mapped[str] = mapped_column(String, nullable=False, default="active")
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.7)
    access_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_accessed_at: Mapped[str | None] = mapped_column(String, nullable=True)


class Goal(Base, IdMixin, TimestampMixin):
    __tablename__ = "goals"

    project_id: Mapped[str | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")
    due_date: Mapped[str | None] = mapped_column(String, nullable=True)


class Task(Base, IdMixin, TimestampMixin):
    __tablename__ = "tasks"

    project_id: Mapped[str | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    goal_id: Mapped[str | None] = mapped_column(ForeignKey("goals.id"), nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    status: Mapped[str] = mapped_column(String, nullable=False, default="open")


class Decision(Base, IdMixin, TimestampMixin):
    __tablename__ = "decisions"

    project_id: Mapped[str | None] = mapped_column(ForeignKey("projects.id"), nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="proposed")


class Episode(Base, IdMixin, TimestampMixin):
    __tablename__ = "episodes"

    title: Mapped[str] = mapped_column(String, nullable=False)
    context: Mapped[str | None] = mapped_column(Text, nullable=True)
    outcome: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.6)


class Procedure(Base, IdMixin, TimestampMixin):
    __tablename__ = "procedures"

    title: Mapped[str] = mapped_column(String, nullable=False)
    steps_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")


class SelfModel(Base, IdMixin, TimestampMixin):
    __tablename__ = "self_model"

    self_name: Mapped[str] = mapped_column(String, nullable=False, default="EvoBrain")
    self_role: Mapped[str] = mapped_column(String, nullable=False, default="cognitive_assistant")
    autonomy_level: Mapped[str] = mapped_column(String, nullable=False, default="assisted")
    current_focus: Mapped[str | None] = mapped_column(String, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.7)


class SystemState(Base, IdMixin, TimestampMixin):
    __tablename__ = "system_state"

    safe_mode: Mapped[str] = mapped_column(String, nullable=False, default="off")
    active_mode: Mapped[str] = mapped_column(String, nullable=False, default="passive")
    last_backup_path: Mapped[str | None] = mapped_column(String, nullable=True)


class SourceProfile(Base, IdMixin, TimestampMixin):
    __tablename__ = "source_profiles"

    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    source_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    source_ref: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")


class SourceFileState(Base, IdMixin, TimestampMixin):
    __tablename__ = "source_file_state"
    __table_args__ = (
        UniqueConstraint("source_profile_id", "file_path", name="uq_source_file_state_profile_path"),
    )

    source_profile_id: Mapped[str] = mapped_column(ForeignKey("source_profiles.id"), nullable=False, index=True)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    mtime_ns: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    content_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    last_document_id: Mapped[str | None] = mapped_column(String, nullable=True)
    last_seen_at: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="active")
