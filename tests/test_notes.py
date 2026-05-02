NOTE_PAYLOAD = {
    "title": "My Note",
    "body_markdown": "# Test\nThis is a note.",
    "note_type": "manual",
    "source_type": "manual",
    "epistemic_type": "fact",
    "confidence": 0.9,
}


def test_create_and_list_note(client):
    r = client.post("/api/v1/notes", json=NOTE_PAYLOAD)
    assert r.status_code == 201
    data = r.json()
    assert data["ok"] is True
    assert data["data"]["title"] == "My Note"
    assert data["data"]["epistemic_type"] == "fact"

    r2 = client.get("/api/v1/notes")
    assert r2.status_code == 200
    assert r2.json()["data"]["total"] == 1


def test_get_note_not_found(client):
    r = client.get("/api/v1/notes/ghost")
    assert r.json()["ok"] is False
    assert r.json()["error"]["code"] == "not_found"


def test_update_note(client):
    r = client.post("/api/v1/notes", json=NOTE_PAYLOAD)
    note_id = r.json()["data"]["id"]

    r2 = client.patch(f"/api/v1/notes/{note_id}", json={"title": "Updated", "epistemic_type": "inference"})
    assert r2.status_code == 200
    assert r2.json()["data"]["title"] == "Updated"
    assert r2.json()["data"]["epistemic_type"] == "inference"


def test_delete_note(client):
    r = client.post("/api/v1/notes", json=NOTE_PAYLOAD)
    note_id = r.json()["data"]["id"]

    r2 = client.delete(f"/api/v1/notes/{note_id}")
    assert r2.json()["data"]["deleted"] is True

    r3 = client.get(f"/api/v1/notes/{note_id}")
    assert r3.json()["ok"] is False


def test_filter_notes_by_document(client):
    r = client.post("/api/v1/documents/import", json={"content": "Source text.", "title": "Src"})
    doc_id = r.json()["data"]["document_id"]

    payload = {**NOTE_PAYLOAD, "document_id": doc_id}
    client.post("/api/v1/notes", json=payload)
    client.post("/api/v1/notes", json=NOTE_PAYLOAD)  # unlinked note

    r2 = client.get(f"/api/v1/notes?document_id={doc_id}")
    assert r2.json()["data"]["total"] == 1
