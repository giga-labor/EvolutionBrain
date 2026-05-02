from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from fastapi import Depends
from app.schemas.chat import ChatQueryRequest, ChatResponse
from app.reasoning.service import ReasoningService
from app.db.session import get_db
from app.audit.service import AuditService

router = APIRouter()


def _estimate_tokens(text: str) -> int:
    # Fast approximation compatible with mixed IT/EN text for per-response telemetry.
    cleaned = " ".join((text or "").split())
    if not cleaned:
        return 0
    return max(1, round(len(cleaned) / 4))


def _extract_external_llm_usage(response: ChatResponse) -> dict | None:
    for action in response.executed_actions or []:
        usage = action.get("llm_usage") if isinstance(action, dict) else None
        if isinstance(usage, dict):
            return usage
    return None


def _attach_token_usage(payload: ChatQueryRequest, response: ChatResponse) -> ChatResponse:
    external_usage = _extract_external_llm_usage(response)
    if external_usage:
        # External provider numbers are treated as authoritative if available.
        input_tokens = int(external_usage.get("input_tokens", 0) or 0)
        output_tokens = int(external_usage.get("output_tokens", 0) or 0)
        total_tokens = int(external_usage.get("total_tokens", input_tokens + output_tokens) or 0)
        provider = external_usage.get("provider", "external_llm")
        model = external_usage.get("model")
        response.token_usage = {
            "source": "external_reported",
            "provider": provider,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        }
        return response

    input_tokens = _estimate_tokens(payload.message)
    output_tokens = _estimate_tokens(response.answer)
    response.token_usage = {
        "source": "estimated",
        "provider": "evobrain_internal",
        "model": None,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }
    return response


def _audit_token_usage(payload: ChatQueryRequest, response: ChatResponse, db: Session) -> None:
    usage = response.token_usage or {}
    if not usage:
        return
    session_or_fallback = payload.session_id or "anonymous"
    AuditService(db).log(
        entity_type="chat",
        entity_id=session_or_fallback,
        action="token_usage_recorded",
        payload={
            "active_mode": response.active_mode,
            "epistemic_type": response.epistemic_type,
            "token_usage": usage,
            "message_preview": (payload.message or "")[:160],
        },
        actor="system",
    )


def _derive_response_report(response: ChatResponse) -> dict:
    confidence = float(response.confidence or 0.0)
    if confidence >= 0.85:
        certainty = "certo"
    elif confidence >= 0.55:
        certainty = "probabile"
    else:
        certainty = "non noto"

    source = "inferenza"
    if response.used_sources:
        source = "memoria consolidata"
    elif response.context_summary and "input corrente" in response.context_summary.lower():
        source = "input corrente"

    executed = len(response.executed_actions or [])
    suggested = len(response.suggested_actions or [])
    if executed > 0:
        action = "azione eseguita"
    elif suggested > 0:
        action = "azione suggerita"
    else:
        action = "nessuna"

    usage = response.token_usage or {}
    return {
        "certainty": certainty,
        "source": source,
        "action": action,
        "token_usage": usage,
    }


@router.post("/query", response_model=ChatResponse)
def query(payload: ChatQueryRequest, db: Session = Depends(get_db)) -> ChatResponse:
    service = ReasoningService(db)
    try:
        response = service.answer_chat(payload)
        response = _attach_token_usage(payload, response)
        response.response_report = _derive_response_report(response)
        _audit_token_usage(payload, response, db)
        return response
    except OperationalError as exc:
        if "disk is full" in str(exc).lower() or "database or disk" in str(exc).lower():
            response = ChatResponse(
                answer="Errore: spazio su disco insufficiente. Libera spazio su D: per continuare.",
                epistemic_type="error",
                confidence=0.0,
                used_sources=[],
                used_objects=[],
                suggested_actions=[{"type": "free_disk_space"}],
                executed_actions=[],
                active_mode="error",
                context_summary="Disco pieno.",
            )
            response = _attach_token_usage(payload, response)
            response.response_report = _derive_response_report(response)
            _audit_token_usage(payload, response, db)
            return response
        raise HTTPException(status_code=500, detail=str(exc)) from exc
