import asyncio
import logging
from datetime import datetime, timezone

logger = logging.getLogger("evobrain.scheduler")

# Intervals in seconds
_DAILY = 86400
_WEEKLY = 604800
_JOB_POLL = 30


class EvoBrainScheduler:
    """Lightweight asyncio-based scheduler for periodic cognitive maintenance tasks."""

    def __init__(self):
        self._tasks: list[asyncio.Task] = []

    def start(self):
        self._tasks = [
            asyncio.create_task(self._run_periodic(self._job_queue_processor, _JOB_POLL, "job_queue_processor")),
            asyncio.create_task(self._run_periodic(self._daily_memory_recalculate, _DAILY, "daily_memory")),
            asyncio.create_task(self._run_periodic(self._daily_goals_reprioritize, _DAILY, "daily_goals")),
            asyncio.create_task(self._run_periodic(self._daily_backup, _DAILY, "daily_backup")),
            asyncio.create_task(self._run_periodic(self._weekly_contradiction_scan, _WEEKLY, "weekly_contradictions")),
            asyncio.create_task(self._run_periodic(self._weekly_drift_detection, _WEEKLY, "weekly_drift")),
        ]
        logger.info("EvoBrain scheduler started with %d tasks", len(self._tasks))

    def stop(self):
        for t in self._tasks:
            t.cancel()
        logger.info("EvoBrain scheduler stopped")

    @staticmethod
    async def _run_periodic(coro_fn, interval_seconds: int, name: str):
        while True:
            try:
                await coro_fn()
            except asyncio.CancelledError:
                logger.info("Scheduler task '%s' cancelled", name)
                return
            except Exception as exc:
                logger.error("Scheduler task '%s' error: %s", name, exc)
            await asyncio.sleep(interval_seconds)

    @staticmethod
    async def _job_queue_processor():
        from app.core.job_worker import JobWorker
        worker = JobWorker()
        await worker._process_one()

    @staticmethod
    async def _daily_memory_recalculate():
        from app.db.session import SessionLocal
        from app.memory.service import MemoryService
        with SessionLocal() as db:
            svc = MemoryService(db)
            result = svc.recalculate()
            auto_result = svc.auto_promote_demote()
            logger.info(
                "Daily memory: recalculated=%d, promoted=%d, demoted=%d",
                result["updated"], auto_result["promoted_count"], auto_result["demoted_count"]
            )

    @staticmethod
    async def _daily_goals_reprioritize():
        from app.db.session import SessionLocal
        from app.goals.service import GoalService
        with SessionLocal() as db:
            result = GoalService(db).recalculate_priorities()
            logger.info("Daily goals reprioritized: %d updated", result["updated"])

    @staticmethod
    async def _daily_backup():
        from app.db.session import SessionLocal
        from app.core.config import get_settings
        from app.platform.backup_service import BackupService
        from app.db.repositories.system_state import SystemStateRepo
        settings = get_settings()
        try:
            svc = BackupService(settings.database_url)
            backup_path = svc.create_backup()
            with SessionLocal() as db:
                SystemStateRepo(db).update_singleton(last_backup_path=backup_path)
            logger.info("Daily backup created: %s", backup_path)
        except Exception as exc:
            logger.error("Daily backup failed: %s", exc)

    @staticmethod
    async def _weekly_contradiction_scan():
        from app.db.session import SessionLocal
        from app.db.models import Relation
        with SessionLocal() as db:
            contradictions = (
                db.query(Relation)
                .filter(Relation.relation_type == "contradicts")
                .all()
            )
            logger.info("Weekly contradiction scan: %d contradicting relations found", len(contradictions))

    @staticmethod
    async def _weekly_drift_detection():
        from app.db.session import SessionLocal
        from app.db.models import Relation
        with SessionLocal() as db:
            low_confidence = (
                db.query(Relation)
                .filter(Relation.confidence < 0.35)
                .all()
            )
            logger.info("Weekly drift detection: %d low-confidence relations", len(low_confidence))
