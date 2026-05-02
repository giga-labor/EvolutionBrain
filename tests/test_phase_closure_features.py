def test_tasks_decisions_episodes_procedures_self_model(client):
    p = client.post("/api/v1/projects", json={"name": "Phase Close"}).json()["data"]
    g = client.post("/api/v1/goals", json={"project_id": p["id"], "title": "Gate G3"}).json()["data"]

    t = client.post(
        "/api/v1/tasks",
        json={"project_id": p["id"], "goal_id": g["id"], "title": "Implement task route"},
    )
    assert t.status_code == 201

    d = client.post("/api/v1/decisions", json={"project_id": p["id"], "title": "Use hybrid search"})
    assert d.status_code == 201

    e = client.post("/api/v1/episodes", json={"title": "Episode 1", "context": "Runtime", "outcome": "ok"})
    assert e.status_code == 201

    proc = client.post("/api/v1/procedures", json={"title": "Procedure 1", "steps_markdown": "1. step"})
    assert proc.status_code == 201

    sm = client.get("/api/v1/self-model")
    assert sm.status_code == 200
    upd = client.put("/api/v1/self-model", json={"current_focus": "phase_closure"})
    assert upd.status_code == 200
    assert upd.json()["data"]["current_focus"] == "phase_closure"


def test_attention_meta_maintenance_and_ui(client):
    c1 = client.post("/api/v1/concepts", json={"name": "A", "description": "topic A"}).json()["data"]
    c2 = client.post("/api/v1/concepts", json={"name": "B", "description": "topic B"}).json()["data"]
    client.post("/api/v1/relations", json={"source_id": c1["id"], "target_id": c2["id"], "relation_type": "supports"})
    client.post("/api/v1/relations", json={"source_id": c1["id"], "target_id": c2["id"], "relation_type": "contradicts"})

    focus = client.post("/api/v1/attention/focus", json={"candidates": [{"id": "x", "score": 0.2}, {"id": "y", "score": 0.9}]})
    assert focus.status_code == 200
    assert focus.json()["data"]["focus"]["id"] == "y"

    meta = client.post("/api/v1/meta/evaluate", json={"confidence": 0.9, "used_sources": [{"id": "1"}]})
    assert meta.status_code == 200
    assert meta.json()["data"]["overconfidence_risk"] in {"high", "low"}

    contradictions = client.post("/api/v1/maintenance/contradictions")
    assert contradictions.status_code == 200
    assert contradictions.json()["data"]["conflict_count"] >= 1

    drift = client.post("/api/v1/maintenance/drift")
    assert drift.status_code == 200
    assert drift.json()["ok"] is True

    ui_dash = client.get("/api/v1/ui/dashboard")
    assert ui_dash.status_code == 200
    assert "EvoBrain Dashboard" in ui_dash.text
    ui_graph = client.get("/api/v1/ui/graph")
    assert ui_graph.status_code == 200
    assert "EvoBrain Graph" in ui_graph.text
    ui_audit = client.get("/api/v1/ui/audit")
    assert ui_audit.status_code == 200
    assert "Audit Console" in ui_audit.text


def test_safe_mode_and_backup_restore(client):
    on = client.post("/api/v1/system/safe-mode?mode=on")
    assert on.status_code == 200
    assert on.json()["safe_mode"] == "on"

    blocked = client.post("/api/v1/notes", json={"title": "Blocked", "body_markdown": "x", "note_type": "manual", "source_type": "manual"})
    assert blocked.status_code == 423

    off = client.post("/api/v1/system/safe-mode?mode=off")
    assert off.status_code == 200
    assert off.json()["safe_mode"] == "off"

    ok = client.post("/api/v1/notes", json={"title": "Allowed", "body_markdown": "x", "note_type": "manual", "source_type": "manual"})
    assert ok.status_code == 201

    backup = client.post("/api/v1/system/backup")
    assert backup.status_code == 200
    backup_path = backup.json()["backup_path"]

    restore = client.post(f"/api/v1/system/restore?backup_path={backup_path}")
    assert restore.status_code == 200
    assert restore.json()["ok"] is True
