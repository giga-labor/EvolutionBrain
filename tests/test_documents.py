def test_list_documents_empty(client):
    r = client.get("/api/v1/documents")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["data"]["items"] == []
    assert data["data"]["total"] == 0


def test_import_document(client):
    r = client.post("/api/v1/documents/import", json={
        "content": "Hello EvoBrain, this is a test document.",
        "title": "Test Doc",
        "source_type": "text",
        "source_ref": "https://example.com/test-doc",
    })
    assert r.status_code == 201
    data = r.json()
    assert data["ok"] is True
    assert data["data"]["document_id"] is not None
    assert data["data"]["status"] == "created"

    r_get = client.get(f"/api/v1/documents/{data['data']['document_id']}")
    assert r_get.status_code == 200
    assert r_get.json()["data"]["source_ref"] == "https://example.com/test-doc"


def test_import_duplicate_detected(client):
    payload = {"content": "Same content, different day.", "title": "Dup"}
    client.post("/api/v1/documents/import", json=payload)
    r = client.post("/api/v1/documents/import", json=payload)
    assert r.status_code == 201
    assert r.json()["data"]["status"] == "duplicate"


def test_get_document_after_import(client):
    r = client.post("/api/v1/documents/import", json={"content": "Fetchable content.", "title": "Fetch"})
    doc_id = r.json()["data"]["document_id"]

    r2 = client.get(f"/api/v1/documents/{doc_id}")
    assert r2.status_code == 200
    data = r2.json()
    assert data["ok"] is True
    assert data["data"]["id"] == doc_id
    assert data["data"]["title"] == "Fetch"


def test_get_document_not_found(client):
    r = client.get("/api/v1/documents/does-not-exist")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert data["error"]["code"] == "not_found"


def test_update_document(client):
    r = client.post("/api/v1/documents/import", json={"content": "Update me.", "title": "Old"})
    doc_id = r.json()["data"]["document_id"]

    r2 = client.patch(f"/api/v1/documents/{doc_id}", json={"title": "New Title"})
    assert r2.status_code == 200
    assert r2.json()["data"]["title"] == "New Title"


def test_delete_document(client):
    r = client.post("/api/v1/documents/import", json={"content": "Delete me.", "title": "Del"})
    doc_id = r.json()["data"]["document_id"]

    r2 = client.delete(f"/api/v1/documents/{doc_id}")
    assert r2.status_code == 200
    assert r2.json()["data"]["deleted"] is True

    r3 = client.get(f"/api/v1/documents/{doc_id}")
    assert r3.json()["ok"] is False
