from fastapi import APIRouter
from app.api.routes import (
    system,
    chat,
    documents,
    notes,
    projects,
    search,
    jobs,
    concepts,
    relations,
    goals,
    memory,
    audit,
    actions,
    simulation,
    adaptation,
    tasks,
    decisions,
    episodes,
    procedures,
    self_model,
    attention,
    metacognition,
    maintenance,
    sources,
    ui,
)

api_router = APIRouter()
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(decisions.router, prefix="/decisions", tags=["decisions"])
api_router.include_router(concepts.router, prefix="/concepts", tags=["concepts"])
api_router.include_router(relations.router, prefix="/relations", tags=["relations"])
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
api_router.include_router(episodes.router, prefix="/episodes", tags=["episodes"])
api_router.include_router(procedures.router, prefix="/procedures", tags=["procedures"])
api_router.include_router(self_model.router, prefix="/self-model", tags=["self-model"])
api_router.include_router(attention.router, prefix="/attention", tags=["attention"])
api_router.include_router(metacognition.router, prefix="/meta", tags=["metacognition"])
api_router.include_router(maintenance.router, prefix="/maintenance", tags=["maintenance"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
api_router.include_router(actions.router, prefix="/actions", tags=["actions"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["simulation"])
api_router.include_router(adaptation.router, prefix="/adaptation", tags=["adaptation"])
api_router.include_router(ui.router, prefix="/ui", tags=["ui"])
