from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
