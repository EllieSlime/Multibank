from http import HTTPStatus


def test_health(test_client):
    resp = test_client.get("/health")
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()["status"] == "healthy"


def test_create_and_get_question(test_client):
    # Create
    payload = {"text": "What is FastAPI?"}
    create_resp = test_client.post("/api/v1/questions/", json=payload)
    assert create_resp.status_code == HTTPStatus.OK
    data = create_resp.json()
    assert data["text"] == payload["text"]
    qid = data["id"]

    # List (returns list[str])
    list_resp = test_client.get("/api/v1/questions/")
    assert list_resp.status_code == HTTPStatus.OK
    assert payload["text"] in list_resp.json()

    # Get by id (with answers array)
    get_resp = test_client.get(f"/api/v1/questions/{qid}")
    assert get_resp.status_code == HTTPStatus.OK
    q = get_resp.json()
    assert q["id"] == qid
    assert q["text"] == payload["text"]
    assert isinstance(q["answers"], list)


def test_delete_question(test_client):
    # Create
    payload = {"text": "To be deleted"}
    create_resp = test_client.post("/api/v1/questions/", json=payload)
    qid = create_resp.json()["id"]

    # Delete
    del_resp = test_client.delete(f"/api/v1/questions/{qid}")
    assert del_resp.status_code == HTTPStatus.OK
    assert "deleted successfully" in del_resp.json()["message"]

    # Verify 404 on get
    get_resp = test_client.get(f"/api/v1/questions/{qid}")
    assert get_resp.status_code == HTTPStatus.NOT_FOUND


