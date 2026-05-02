from enum import StrEnum


class EpistemicType(StrEnum):
    FACT = "fact"
    INFERENCE = "inference"
    HYPOTHESIS = "hypothesis"
    SUGGESTION = "suggestion"
    VERIFY = "verify"
    SCENARIO = "scenario"
    CONFLICT = "conflict"
    UNKNOWN = "unknown"


class MemoryLayer(StrEnum):
    RAW = "raw"
    PROCESSED = "processed"
    ACTIVE = "active"
    CONTEXTUAL = "contextual"
    STRATEGIC = "strategic"
    HISTORICAL = "historical"
    LATENT = "latent"
    TEMPORARY = "temporary"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    RETRYING = "retrying"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    AWAITING_VALIDATION = "awaiting_validation"
