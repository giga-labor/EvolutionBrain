def test_sources_profiles_and_import_usage(client):
    src = client.post(
        "/api/v1/sources",
        json={"name": "Repo Docs", "source_type": "folder", "source_ref": "D:\\\\PROGETTI\\\\docs"},
    )
    assert src.status_code == 201
    src_data = src.json()["data"]
    assert src_data["name"] == "Repo Docs"

    listed = client.get("/api/v1/sources")
    assert listed.status_code == 200
    assert listed.json()["data"]["total"] >= 1

    imp = client.post(
        "/api/v1/documents/import",
        json={
            "title": "Imported with source profile",
            "source_type": src_data["source_type"],
            "source_ref": src_data["source_ref"],
            "content": "content from source profile",
        },
    )
    assert imp.status_code == 201
    doc_id = imp.json()["data"]["document_id"]

    get_doc = client.get(f"/api/v1/documents/{doc_id}")
    assert get_doc.status_code == 200
    assert get_doc.json()["data"]["source_ref"].endswith("docs")

    delete_src = client.delete(f"/api/v1/sources/{src_data['id']}")
    assert delete_src.status_code == 200
