SAFE_MODE = "off"


def get_safe_mode() -> str:
    return SAFE_MODE


def set_safe_mode(mode: str) -> str:
    global SAFE_MODE
    SAFE_MODE = mode
    return SAFE_MODE


def sync_from_db(db) -> str:
    """Sync SAFE_MODE from SystemState DB row on startup so it survives restarts."""
    global SAFE_MODE
    try:
        from app.db.repositories.system_state import SystemStateRepo
        state = SystemStateRepo(db).get_singleton()
        SAFE_MODE = state.safe_mode or "off"
    except Exception:
        pass
    return SAFE_MODE
