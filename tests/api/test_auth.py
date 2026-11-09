from fastapi.testclient import TestClient


def test_register_returns_201_without_password(client: TestClient) -> None:
    response = client.post(
        "/auth/register",
        json={
            "username": "liran",
            "email": "liran@example.com",
            "password": "mypassword123",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "liran"
    assert "password_hash" not in body
