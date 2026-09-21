import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        response = test_client.post(
            "/token",
            json={
                "username": "admin",
                "password": "finshield123"
            }
        )

        assert response.status_code == 200, response.text

        token = response.json()["access_token"]
        test_client.headers.update({
            "Authorization": f"Bearer {token}"
        })

        yield test_client