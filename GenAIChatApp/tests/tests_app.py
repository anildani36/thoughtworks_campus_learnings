from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_session():
    response = client.post("/sessions", json={"session_user": "  NewUser "})
    assert response.status_code == 200
    data = response.json()
    assert data["session_user"] == "newuser"
    assert "session_id" in data
    assert "created_at" in data


def test_create_session_empty_user():
    response = client.post("/sessions", json={"session_user": "   "})
    assert response.status_code == 422  # validation error


def test_add_message_valid():
    create_res = client.post("/sessions", json={"session_user": "test"})
    session_id = create_res.json()["session_id"]

    response = client.post(f"/sessions/{session_id}/messages", json={
        "role": "user",
        "content": "What is AI?"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Message added successfully"


def test_add_message_invalid_session():
    response = client.post("/sessions/999/messages", json={
        "role": "user",
        "content": "Is this valid?"
    })
    assert response.status_code == 404


def test_add_message_invalid_role():
    create_res = client.post("/sessions", json={"session_user": "test2"})
    session_id = create_res.json()["session_id"]

    response = client.post(f"/sessions/{session_id}/messages", json={
        "role": "bot",
        "content": "Wrong role"
    })

    assert response.status_code == 400


def test_get_messages():
    create_res = client.post("/sessions", json={"session_user": "user1"})
    session_id = create_res.json()["session_id"]

    client.post(f"/sessions/{session_id}/messages", json={
        "role": "user", "content": "Hello!"
    })
    client.post(f"/sessions/{session_id}/messages", json={
        "role": "assistant", "content": "Hi!"
    })

    res_all = client.get(f"/sessions/{session_id}/messages")
    assert res_all.status_code == 200
    assert len(res_all.json()) == 2

    res_filtered = client.get(f"/sessions/{session_id}/messages", params={"role": "user"})
    assert res_filtered.status_code == 200
    assert len(res_filtered.json()) == 1
    assert res_filtered.json()[0]["role"] == "user"
