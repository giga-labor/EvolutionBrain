def test_search_hybrid_and_chat_grounded(client):
    client.post(
        "/api/v1/documents/import",
        json={"content": "EvoBrain manages memory layers and retrieval.", "title": "Memory Doc"},
    )
    client.post(
        "/api/v1/notes",
        json={
            "title": "Retrieval Note",
            "body_markdown": "Hybrid retrieval combines keyword and semantic signals.",
            "note_type": "manual",
            "source_type": "manual",
        },
    )
    client.post("/api/v1/concepts", json={"name": "Hybrid Retrieval", "description": "Search strategy"})

    search = client.get("/api/v1/search?q=hybrid retrieval&mode=hybrid")
    assert search.status_code == 200
    payload = search.json()["data"]
    assert payload["mode"] == "hybrid"
    assert payload["total"] >= 1

    chat = client.post("/api/v1/chat/query", json={"message": "What do internal sources say about hybrid retrieval?"})
    assert chat.status_code == 200
    body = chat.json()
    assert body["epistemic_type"] in {"inference", "ignorance"}
    assert isinstance(body["used_sources"], list)
    assert "token_usage" in body
    assert body["token_usage"]["total_tokens"] >= 1

    logs = client.get("/api/v1/audit/logs?entity_type=chat&limit=20")
    assert logs.status_code == 200
    items = logs.json()["data"]["items"]
    assert any(i["action"] == "token_usage_recorded" for i in items)
