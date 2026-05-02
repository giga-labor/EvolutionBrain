from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.jobs import JobRepo
from app.audit.service import AuditService
from app.schemas.jobs import JobCreate, JobRead
from app.schemas import common

router = APIRouter()

TERMINAL_STATUSES = {"completed", "failed", "cancelled"}


@router.get("", response_model=common.ApiResponse)
def list_jobs(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    items = JobRepo(db).list(limit=limit, offset=offset)
    reads = [JobRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    job = JobRepo(db).create(**payload.model_dump())
    AuditService(db).log("job", job.id, "create", {"job_type": job.job_type})
    return common.ok(JobRead.model_validate(job).model_dump(mode="json"))


@router.get("/{job_id}", response_model=common.ApiResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = JobRepo(db).get(job_id)
    if not job:
        return common.err("not_found", f"Job '{job_id}' not found")
    return common.ok(JobRead.model_validate(job).model_dump(mode="json"))


@router.patch("/{job_id}/status", response_model=common.ApiResponse)
def update_job_status(job_id: str, new_status: str, db: Session = Depends(get_db)):
    job = JobRepo(db).update_status(job_id, new_status)
    if not job:
        return common.err("not_found", f"Job '{job_id}' not found")
    AuditService(db).log("job", job.id, "status_change", {"status": new_status})
    return common.ok(JobRead.model_validate(job).model_dump(mode="json"))


@router.delete("/{job_id}", response_model=common.ApiResponse)
def delete_job(job_id: str, db: Session = Depends(get_db)):
    job = JobRepo(db).get(job_id)
    if not job:
        return common.err("not_found", f"Job '{job_id}' not found")
    if job.status not in TERMINAL_STATUSES:
        return common.err("conflict", f"Job '{job_id}' must be in a terminal status before deletion")
    JobRepo(db).delete(job_id)
    AuditService(db).log("job", job_id, "delete")
    return common.ok({"deleted": True, "id": job_id})
