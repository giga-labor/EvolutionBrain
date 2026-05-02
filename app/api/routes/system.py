from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.core.config import get_settings
from app.db.repositories.system_state import SystemStateRepo
from app.platform.backup_service import BackupService
from app.audit.service import AuditService
from app.core.runtime_state import set_safe_mode as set_runtime_safe_mode, get_safe_mode

router = APIRouter()


@router.get("/health")
def health(db: Session = Depends(get_db)):
    settings = get_settings()
    state = SystemStateRepo(db).get_singleton()
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {
        "overall_status": "ok" if db_status == "ok" else "degraded",
        "db_status": db_status,
        "vector_status": "not_configured",
        "llm_status": "not_configured",
        "scheduler_status": "enabled" if settings.scheduler_enabled else "disabled",
        "safe_mode": get_safe_mode(),
    }


@router.get("/state")
def state(db: Session = Depends(get_db)):
    settings = get_settings()
    state_item = SystemStateRepo(db).get_singleton()
    return {
        "current_operational_state": "idle",
        "active_mode": state_item.active_mode,
        "autonomy_level": settings.default_autonomy_level,
        "inference_profile": settings.default_inference_profile,
        "active_project_id": None,
        "queue_depth": 0,
        "last_consolidation_at": None,
        "safe_mode": get_safe_mode(),
        "last_backup_path": state_item.last_backup_path,
    }


@router.post("/safe-mode")
def set_safe_mode_state(mode: str, db: Session = Depends(get_db)):
    if mode not in {"on", "off"}:
        return {"ok": False, "error": "mode must be 'on' or 'off'"}
    set_runtime_safe_mode(mode)
    state = SystemStateRepo(db).update_singleton(safe_mode=mode)
    AuditService(db).log("system_state", state.id, "safe_mode_change", {"safe_mode": mode})
    return {"ok": True, "safe_mode": state.safe_mode}


@router.post("/backup")
def create_backup(db: Session = Depends(get_db)):
    settings = get_settings()
    try:
        backup_path = BackupService(
            settings.database_url,
            retention_count=settings.backup_retention_count,
        ).create_backup()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Backup failed: {exc}") from exc
    state = SystemStateRepo(db).update_singleton(last_backup_path=backup_path)
    AuditService(db).log("system_state", state.id, "backup_created", {"backup_path": backup_path})
    return {"ok": True, "backup_path": backup_path}


@router.post("/restore")
def restore_backup(backup_path: str, db: Session = Depends(get_db)):
    settings = get_settings()
    try:
        restored = BackupService(
            settings.database_url,
            retention_count=settings.backup_retention_count,
        ).restore_backup(backup_path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Restore failed: {exc}") from exc
    state = SystemStateRepo(db).update_singleton(last_backup_path=backup_path)
    AuditService(db).log("system_state", state.id, "backup_restored", {"backup_path": backup_path})
    return {"ok": True, "restored_db_path": restored}
