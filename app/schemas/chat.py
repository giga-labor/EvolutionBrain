from pydantic import BaseModel, Field
from typing import Any


class ChatQueryRequest(BaseModel):
    session_id: str | None = None
    message: str = Field(min_length=1)
    project_id: str | None = None
    mode_hint: str | None = None
    allow_external_sources: bool = False
    inference_profile: str | None = None
    dry_run: bool = False


class ChatResponse(BaseModel):
    answer: str
    epistemic_type: str
    confidence: float
    used_sources: list[dict[str, Any]] = []
    used_objects: list[dict[str, Any]] = []
    suggested_actions: list[dict[str, Any]] = []
    executed_actions: list[dict[str, Any]] = []
    active_mode: str
    context_summary: str | None = None
    token_usage: dict[str, Any] | None = None
    response_report: dict[str, Any] | None = None
