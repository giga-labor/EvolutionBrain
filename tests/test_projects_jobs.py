def test_projects_crud(client):
    create = client.post("/api/v1/projects", json={"name": "Alpha", "description": "Project A"})
    assert create.status_code == 201
    pid = create.json()["data"]["id"]

    get_one = client.get(f"/api/v1/projects/{pid}")
    assert get_one.status_code == 200
    assert get_one.json()["data"]["name"] == "Alpha"

    update = client.patch(f"/api/v1/projects/{pid}", json={"status": "paused"})
    assert update.status_code == 200
    assert update.json()["data"]["status"] == "paused"

    delete = client.delete(f"/api/v1/projects/{pid}")
    assert delete.status_code == 200
    assert delete.json()["data"]["deleted"] is True


def test_jobs_crud_and_status_change(client):
    create = client.post("/api/v1/jobs", json={"job_type": "indexing", "priority": 0.9})
    assert create.status_code == 201
    jid = create.json()["data"]["id"]

    status_change = client.patch(f"/api/v1/jobs/{jid}/status?new_status=completed")
    assert status_change.status_code == 200
    assert status_change.json()["data"]["status"] == "completed"

    delete = client.delete(f"/api/v1/jobs/{jid}")
    assert delete.status_code == 200
    assert delete.json()["data"]["deleted"] is True
