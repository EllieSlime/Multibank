from http import HTTPStatus


def test_create_get_delete_answer_flow(test_client):
    # Create question
    q_payload = {"text": "Question for answers"}
    q_resp = test_client.post("/api/v1/questions/", json=q_payload)
    qid = q_resp.json()["id"]

    # Create answer
    a_payload = {"text": "FastAPI is a modern web framework", "user_id": "1"}
    a_resp = test_client.post(f"/api/v1/questions/{qid}/answers/", json=a_payload)
    assert a_resp.status_code == HTTPStatus.OK
    answer = a_resp.json()
    aid = answer["id"]
    assert answer["question_id"] == qid

    # Get answer
    get_resp = test_client.get(f"/api/v1/answers/{aid}")
    assert get_resp.status_code == HTTPStatus.OK
    assert get_resp.json()["id"] == aid

    # Delete answer
    del_resp = test_client.delete(f"/api/v1/answers/{aid}")
    assert del_resp.status_code == HTTPStatus.OK
    assert "deleted successfully" in del_resp.json()["message"]


