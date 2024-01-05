from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_get_activity_type_by_date(client):
    response = client.get("/api/v1/activities/type/date/2024-01-04")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert type(response.json()) == list
    assert "sport_type" in response.json()[0]
    assert response.json()[0]["sport_type"] == "VirtualRide"
