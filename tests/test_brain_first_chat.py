def test_chat_brain_first_uses_compact_internal_memory(client):
    client.post(
        "/api/v1/notes",
        json={
            "title": "Policy token budget",
            "body_markdown": "Usa prima il cervello interno per ridurre i token dell llm.",
            "note_type": "manual",
            "source_type": "manual",
            "epistemic_type": "fact",
            "confidence": 1.0,
        },
    )

    chat = client.post(
        "/api/v1/chat/query",
        json={"message": "usa prima il cervello interno per ridurre i token dell llm?"},
    )
    assert chat.status_code == 200
    body = chat.json()
    assert body["active_mode"] == "brain_first"
    assert "ridurre i token" in body["answer"].lower()
    assert len(body["used_sources"]) == 1


def test_chat_profile_kv_is_returned_compactly_in_brain_first(client):
    client.post(
        "/api/v1/notes",
        json={
            "title": "KV::utente::stile risposta",
            "body_markdown": "utente | stile risposta | breve e concreta",
            "note_type": "profile_kv",
            "source_type": "chat",
            "epistemic_type": "fact",
            "confidence": 1.0,
        },
    )

    chat = client.post(
        "/api/v1/chat/query",
        json={"message": "utente stile risposta?"},
    )
    assert chat.status_code == 200
    body = chat.json()
    assert body["active_mode"] == "brain_first"
    assert body["answer"] == "breve e concreta"


def test_chat_brain_first_global_for_general_internal_knowledge(client):
    client.post(
        "/api/v1/documents/import",
        json={
            "title": "Recupero interno",
            "content": "EvoBrain usa retrieval ibrido interno con priorita alla memoria consolidata.",
        },
    )

    chat = client.post(
        "/api/v1/chat/query",
        json={"message": "come funziona il recupero interno?"},
    )
    assert chat.status_code == 200
    body = chat.json()
    assert body["active_mode"] in {"brain_first_global", "inference", "brain_first"}
    assert isinstance(body["used_sources"], list)
    assert len(body["used_sources"]) >= 1
