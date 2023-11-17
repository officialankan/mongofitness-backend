from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_redoc(client):
    response = client.get("/redoc")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

def test_get_daily_steps(client):
    response = client.get("/api/v1/steps/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert type(response.json()) == list

def test_get_daily_steps_by_date(client):
    response = client.get("/api/v1/steps/2023-11-01")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert type(response.json()) == dict
    assert "ts" in response.json()
    assert "steps" in response.json()

def test_get_daily_steps_by_date_not_found(client):
    response = client.get("/api/v1/steps/1961-01-01")
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"
    assert type(response.json()) == dict
    assert "detail" in response.json()
    assert response.json()["detail"] == "No daily steps found for 1961-01-01"

def test_get_daily_steps_by_date_invalid_date(client):
    response = client.get("/api/v1/steps/12345")
    assert response.status_code == 422
    assert response.headers["content-type"] == "application/json"
    assert type(response.json()) == dict
    assert "detail" in response.json()
    assert response.json()["detail"][0]["msg"] == "Datetimes provided to dates should have zero time - e.g. be exact dates"

def test_get_daily_steps_by_range(client):
    response = client.get("/api/v1/steps/range/?start=2023-11-01&end=2023-11-10")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert type(response.json()) == list
    assert len(response.json()) == 10
    for item in response.json():
        assert "ts" in item
        assert "steps" in item
