def test_health(client):
    r = client.get("/api/v1/system/health")
    assert r.status_code == 200
    data = r.json()
    assert data["overall_status"] == "ok"
    assert data["db_status"] == "ok"
