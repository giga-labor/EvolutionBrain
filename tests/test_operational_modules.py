def test_actions_adaptation_simulation(client):
    plan = client.post("/api/v1/actions/plan", json={"type": "create_note"})
    assert plan.status_code == 200
    assert plan.json()["ok"] is True
    assert plan.json()["data"]["action_type"] == "create_note"

    blocked = client.post("/api/v1/actions/execute", json={"type": "delete_note"})
    assert blocked.status_code == 200
    assert blocked.json()["data"]["status"] == "blocked"

    # Create a note first so we have a valid target_id to delete
    created = client.post("/api/v1/actions/execute", json={
        "type": "create_note",
        "payload": {"title": "To Delete", "body_markdown": "x", "note_type": "manual", "source_type": "manual"},
    })
    assert created.json()["data"]["executed"] is True
    note_id = created.json()["data"]["result_id"]

    executed = client.post("/api/v1/actions/execute", json={"type": "delete_note", "confirmed": True, "target_id": note_id})
    assert executed.status_code == 200
    assert executed.json()["data"]["executed"] is True

    feedback = client.post("/api/v1/adaptation/feedback", json={"rating": 5, "comment": "useful"})
    assert feedback.status_code == 200
    assert feedback.json()["data"]["status"] == "ok"

    sim = client.post(
        "/api/v1/simulation/run",
        json={"title": "Memory policy", "premise": "policy test", "options": ["Conservative scoring", "Aggressive scoring"]},
    )
    assert sim.status_code == 200
    assert sim.json()["data"]["status"] == "ok"
    assert sim.json()["data"]["epistemic_type"] == "scenario"
