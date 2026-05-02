from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.projects import ProjectRepo
from app.audit.service import AuditService
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectRead
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def list_projects(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    items = ProjectRepo(db).list(limit=limit, offset=offset)
    reads = [ProjectRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = ProjectRepo(db).create(**payload.model_dump())
    AuditService(db).log("project", project.id, "create")
    return common.ok(ProjectRead.model_validate(project).model_dump(mode="json"))


@router.get("/{project_id}", response_model=common.ApiResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = ProjectRepo(db).get(project_id)
    if not project:
        return common.err("not_found", f"Project '{project_id}' not found")
    return common.ok(ProjectRead.model_validate(project).model_dump(mode="json"))


@router.patch("/{project_id}", response_model=common.ApiResponse)
def update_project(project_id: str, payload: ProjectUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    project = ProjectRepo(db).update(project_id, **updates)
    if not project:
        return common.err("not_found", f"Project '{project_id}' not found")
    AuditService(db).log("project", project.id, "update", updates)
    return common.ok(ProjectRead.model_validate(project).model_dump(mode="json"))


@router.delete("/{project_id}", response_model=common.ApiResponse)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    deleted = ProjectRepo(db).delete(project_id)
    if not deleted:
        return common.err("not_found", f"Project '{project_id}' not found")
    AuditService(db).log("project", project_id, "delete")
    return common.ok({"deleted": True, "id": project_id})
