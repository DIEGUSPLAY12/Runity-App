import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_current_user

client = TestClient(app)

FAKE_USER_ID = "12345678-1234-5678-1234-567812345678"

def override_get_current_user():
    return FAKE_USER_ID

app.dependency_overrides[get_current_user] = override_get_current_user

def test_get_feed_empty_state():
    """Prueba que el feed devuelve un formato correcto incluso si no hay actividad."""
    response = client.get("/api/v1/feed/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)
    assert "total" in data
    assert data["page"] == 1

def test_get_feed_pagination():
    """Prueba que los parámetros de paginación se aplican y no dan error."""
    response = client.get("/api/v1/feed/?page=2&per_page=5")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["page"] == 2
    assert data["per_page"] == 5