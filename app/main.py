import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import Response

from app.api.router import api_router
from app.core.config import get_settings
from app.core.runtime_state import get_safe_mode, sync_from_db
from app.core.scheduler import EvoBrainScheduler
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.db import models  # noqa: F401

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("evobrain")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        sync_from_db(db)
    scheduler = None
    if settings.scheduler_enabled:
        scheduler = EvoBrainScheduler()
        scheduler.start()
        logger.info("EvoBrain started - DB tables ensured, scheduler running")
    else:
        logger.info("EvoBrain started - DB tables ensured, scheduler disabled")
    yield
    if scheduler is not None:
        scheduler.stop()
    logger.info("EvoBrain shutting down")


app = FastAPI(title=settings.app_name, lifespan=lifespan)


@app.middleware("http")
async def safe_mode_guard(request, call_next):
    if get_safe_mode() == "on":
        path = request.url.path
        method = request.method.upper()
        allowed = (
            path.startswith("/api/v1/system")
            or method in {"GET", "HEAD", "OPTIONS"}
            or path.startswith("/api/v1/chat/query")
            or path.startswith("/api/v1/search")
            or path.startswith("/api/v1/ui/")
        )
        if not allowed:
            await request.body()  # drain body to avoid anyio.WouldBlock in BaseHTTPMiddleware
            return JSONResponse(
                status_code=423,
                content={
                    "ok": False,
                    "error": {
                        "code": "safe_mode",
                        "message": "Operation blocked by safe mode",
                    },
                },
            )
    return await call_next(request)


@app.get("/")
def root() -> dict:
    return {
        "app": settings.app_name,
        "status": "ok",
        "environment": settings.app_env,
    }


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    return Response(status_code=204)


app.include_router(api_router, prefix="/api/v1")
