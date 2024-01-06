from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_get_activity_type_by_date_range(client):
    response = client.get("/api/v1/activities/type/range/?start=2023-12-20&end=2024-01-06")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert type(response.json()) == list
    assert type(response.json()[0]) == dict
    assert "ts" in response.json()[0]
    assert "sport_type" in response.json()[0]
