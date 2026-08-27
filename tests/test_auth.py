from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200


def test_login_invalid_user():
    response = client.post(
        "/login",
        json={
            "username": "unknown",
            "password": "123"
        }
    )

    assert response.status_code == 401