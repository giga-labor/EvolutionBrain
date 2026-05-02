def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["app"] == "EvoBrain"
    assert data["status"] == "ok"
