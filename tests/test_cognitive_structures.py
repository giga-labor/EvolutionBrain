def test_concepts_relations_goals_memory_and_audit(client):
    c1 = client.post("/api/v1/concepts", json={"name": "Memory", "description": "Long-term structure"}).json()["data"]
    c2 = client.post("/api/v1/concepts", json={"name": "Attention", "description": "Focus mechanism"}).json()["data"]

    rel = client.post(
        "/api/v1/relations",
        json={
            "source_id": c1["id"],
            "target_id": c2["id"],
            "relation_type": "supports",
            "confidence": 0.8,
        },
    )
    assert rel.status_code == 201
    assert rel.json()["data"]["relation_type"] == "supports"

    project = client.post("/api/v1/projects", json={"name": "Cognitive Core"}).json()["data"]
    goal = client.post(
        "/api/v1/goals",
        json={"project_id": project["id"], "title": "Implement memory scoring", "priority": 0.7},
    )
    assert goal.status_code == 201

    memory = client.post(
        "/api/v1/memory/items",
        json={"object_type": "concept", "object_id": c1["id"], "layer": "active", "confidence": 0.9},
    )
    assert memory.status_code == 201
    mid = memory.json()["data"]["id"]

    touched = client.get(f"/api/v1/memory/items/{mid}")
    assert touched.status_code == 200
    assert touched.json()["data"]["access_count"] >= 1

    recalculated = client.post("/api/v1/memory/recalculate")
    assert recalculated.status_code == 200
    assert recalculated.json()["data"]["status"] == "ok"

    goal_recalc = client.post("/api/v1/goals/recalculate")
    assert goal_recalc.status_code == 200
    assert goal_recalc.json()["data"]["recalculated"] is True

    logs = client.get("/api/v1/audit/logs?entity_type=goal")
    assert logs.status_code == 200
    assert logs.json()["data"]["total"] >= 1
