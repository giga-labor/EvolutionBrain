from uuid import uuid4
from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Any


class Meta(BaseModel):
    request_id: str
    timestamp: str
    warnings: list[str] = []


class ApiResponse(BaseModel):
    ok: bool
    data: dict[str, Any] | None
    meta: Meta
    error: dict[str, Any] | None = None


def ok(data: dict[str, Any] | None = None, warnings: list[str] | None = None) -> ApiResponse:
    return ApiResponse(
        ok=True,
        data=data,
        meta=Meta(
            request_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            warnings=warnings or [],
        ),
    )


def err(code: str, message: str) -> ApiResponse:
    return ApiResponse(
        ok=False,
        data=None,
        meta=Meta(
            request_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
        ),
        error={"code": code, "message": message},
    )
