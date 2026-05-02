from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Relation
from app.db.repositories.jobs import JobRepo
from app.audit.service import AuditService
from app.schemas import common

router = APIRouter()


@router.post("/contradictions", response_model=common.ApiResponse)
def contradiction_scan(db: Session = Depends(get_db)):
    relations = db.query(Relation).all()
    pairs: dict[tuple[str, str], set[str]] = {}
    for rel in relations:
        key = (rel.source_id, rel.target_id)
        pairs.setdefault(key, set()).add(rel.relation_type)

    conflicts = []
    for (src, dst), rel_types in pairs.items():
        if "supports" in rel_types and "contradicts" in rel_types:
            conflicts.append({"source_id": src, "target_id": dst, "types": sorted(rel_types)})

    report = {"conflicts": conflicts, "total_relations": len(relations), "conflict_count": len(conflicts)}
    JobRepo(db).create(job_type="contradiction_scan_report", priority=0.4, status="completed")
    AuditService(db).log("maintenance", "contradiction_scan", "run", report)
    return common.ok(report)


@router.post("/drift", response_model=common.ApiResponse)
def drift_detection(db: Session = Depends(get_db)):
    relations = db.query(Relation).all()
    low_conf = [r for r in relations if r.confidence < 0.35]
    report = {
        "total_relations": len(relations),
        "low_confidence_relations": len(low_conf),
        "drift_risk": "high" if len(low_conf) >= 5 else "low",
    }
    JobRepo(db).create(job_type="drift_detection_report", priority=0.4, status="completed")
    AuditService(db).log("maintenance", "drift_detection", "run", report)
    return common.ok(report)
