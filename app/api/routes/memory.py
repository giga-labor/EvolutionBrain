from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.repositories.memory_items import MemoryItemRepo
from app.audit.service import AuditService
from app.memory.service import MemoryService
from app.schemas.memory import MemoryItemCreate, MemoryItemRead, MemoryItemUpdate
from app.schemas import common

router = APIRouter()


@router.get("/items", response_model=common.ApiResponse)
def list_memory_items(
    limit: int = 100,
    offset: int = 0,
    layer: str | None = None,
    db: Session = Depends(get_db),
):
    items = MemoryItemRepo(db).list(limit=limit, offset=offset, layer=layer)
    reads = [MemoryItemRead.model_validate(i).model_dump(mode="json") for i in items]
    return common.ok({"items": reads, "total": len(reads)})


@router.post("/items", response_model=common.ApiResponse, status_code=status.HTTP_201_CREATED)
def create_memory_item(payload: MemoryItemCreate, db: Session = Depends(get_db)):
    item = MemoryItemRepo(db).create(**payload.model_dump())
    AuditService(db).log("memory_item", item.id, "create")
    return common.ok(MemoryItemRead.model_validate(item).model_dump(mode="json"))


@router.get("/items/{memory_id}", response_model=common.ApiResponse)
def get_memory_item(memory_id: str, db: Session = Depends(get_db)):
    item = MemoryItemRepo(db).get(memory_id)
    if not item:
        return common.err("not_found", f"Memory item '{memory_id}' not found")
    MemoryItemRepo(db).touch(memory_id)
    refreshed = MemoryItemRepo(db).get(memory_id)
    return common.ok(MemoryItemRead.model_validate(refreshed).model_dump(mode="json"))


@router.patch("/items/{memory_id}", response_model=common.ApiResponse)
def update_memory_item(memory_id: str, payload: MemoryItemUpdate, db: Session = Depends(get_db)):
    updates = payload.model_dump(exclude_none=True)
    item = MemoryItemRepo(db).update(memory_id, **updates)
    if not item:
        return common.err("not_found", f"Memory item '{memory_id}' not found")
    AuditService(db).log("memory_item", item.id, "update", updates)
    return common.ok(MemoryItemRead.model_validate(item).model_dump(mode="json"))


@router.post("/recalculate", response_model=common.ApiResponse)
def recalculate_memory(scope: str = "all", db: Session = Depends(get_db)):
    result = MemoryService(db).recalculate(scope=scope)
    AuditService(db).log("memory_item", "all", "recalculate", result)
    return common.ok(result)


@router.delete("/items/{memory_id}", response_model=common.ApiResponse)
def delete_memory_item(memory_id: str, db: Session = Depends(get_db)):
    deleted = MemoryItemRepo(db).delete(memory_id)
    if not deleted:
        return common.err("not_found", f"Memory item '{memory_id}' not found")
    AuditService(db).log("memory_item", memory_id, "delete")
    return common.ok({"deleted": True, "id": memory_id})


@router.post("/promote/{memory_id}", response_model=common.ApiResponse)
def promote_memory_item(
    memory_id: str,
    target_layer: str,
    actor: str = "user",
    db: Session = Depends(get_db),
):
    result = MemoryService(db).promote(memory_id, target_layer, actor=actor)
    if not result.get("ok"):
        return common.err("promotion_failed", result.get("error", "promotion failed"))
    return common.ok(result)


@router.post("/demote/{memory_id}", response_model=common.ApiResponse)
def demote_memory_item(
    memory_id: str,
    target_layer: str,
    actor: str = "user",
    db: Session = Depends(get_db),
):
    result = MemoryService(db).demote(memory_id, target_layer, actor=actor)
    if not result.get("ok"):
        return common.err("demotion_failed", result.get("error", "demotion failed"))
    return common.ok(result)


@router.post("/auto-update", response_model=common.ApiResponse)
def auto_update_memory(actor: str = "system", db: Session = Depends(get_db)):
    result = MemoryService(db).auto_promote_demote(actor=actor)
    AuditService(db).log(
        "memory_item", "all", "memory.auto_update",
        {"promoted": result["promoted_count"], "demoted": result["demoted_count"]},
    )
    return common.ok(result)
