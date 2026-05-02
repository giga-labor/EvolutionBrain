from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.episodes import EpisodeRepo
from app.audit.service import AuditService
from app.schemas.episodes import EpisodeCreate, EpisodeRead, EpisodeUpdate
from app.schemas import common

router = APIRouter()


@router.get("", response_model=common.ApiResponse)
def list_episodes(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    items = EpisodeRepo(db).list(limit=limit, offset=offset)
    reads = [EpisodeRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_episode(payload: EpisodeCreate, db: Session = Depends(get_db)):
    item = EpisodeRepo(db).create(**payload.model_dump())
    AuditService(db).log("episode", item.id, "create")
    return common.ok(EpisodeRead.model_validate(item).model_dump(mode="json"))


@router.get("/{episode_id}", response_model=common.ApiResponse)
def get_episode(episode_id: str, db: Session = Depends(get_db)):
    item = EpisodeRepo(db).get(episode_id)
    if not item:
        return common.err("not_found", f"Episode '{episode_id}' not found")
    return common.ok(EpisodeRead.model_validate(item).model_dump(mode="json"))


@router.patch("/{episode_id}", response_model=common.ApiResponse)
def update_episode(episode_id: str, payload: EpisodeUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    item = EpisodeRepo(db).update(episode_id, **updates)
    if not item:
        return common.err("not_found", f"Episode '{episode_id}' not found")
    AuditService(db).log("episode", item.id, "update", updates)
    return common.ok(EpisodeRead.model_validate(item).model_dump(mode="json"))


@router.delete("/{episode_id}", response_model=common.ApiResponse)
def delete_episode(episode_id: str, db: Session = Depends(get_db)):
    deleted = EpisodeRepo(db).delete(episode_id)
    if not deleted:
        return common.err("not_found", f"Episode '{episode_id}' not found")
    AuditService(db).log("episode", episode_id, "delete")
    return common.ok({"deleted": True, "id": episode_id})
