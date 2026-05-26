import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_current_user

client = TestClient(app)

CURRENT_USER_ID = "12345678-1234-5678-1234-567812345678"
OTHER_USER_ID = "87654321-4321-8765-4321-876543210987"

def override_get_current_user():
    return CURRENT_USER_ID

app.dependency_overrides[get_current_user] = override_get_current_user

def test_share_session_success():
    """Prueba que un usuario puede compartir su propia sesión."""
    # 1. Crear sesión de prueba
    payload = {
        "start_time": "2026-03-18T10:00:00Z",
        "distance_meters": 5000,
        "duration_seconds": 1500,
        "calories": 350
    }
    res_session = client.post("/api/v1/sessions/", json=payload)
    session_id = res_session.json()["id"]
    
    # 2. Compartirla
    res_share = client.post(f"/api/v1/sessions/{session_id}/share")
    assert res_share.status_code == status.HTTP_201_CREATED

def test_share_session_duplicate_fails():
    """Prueba que salta un error 409 si intentamos compartirla dos veces."""
    payload = {
        "start_time": "2026-03-18T11:00:00Z",
        "distance_meters": 3000,
        "duration_seconds": 900
    }
    res_session = client.post("/api/v1/sessions/", json=payload)
    session_id = res_session.json()["id"]
    
    # Compartir (Primera vez -> OK)
    client.post(f"/api/v1/sessions/{session_id}/share")
    
    # Compartir (Segunda vez -> Falla)
    res_share = client.post(f"/api/v1/sessions/{session_id}/share")
    assert res_share.status_code == status.HTTP_409_CONFLICT

def test_share_unowned_session_fails():
    """Prueba que no podemos compartir las sesiones de otros."""
    # 1. Crear sesión como OTHER_USER
    app.dependency_overrides[get_current_user] = lambda: OTHER_USER_ID
    payload = {
        "start_time": "2026-03-18T12:00:00Z",
        "distance_meters": 1000,
        "duration_seconds": 300
    }
    res_session = client.post("/api/v1/sessions/", json=payload)
    session_id = res_session.json()["id"]
    
    # 2. Intentar compartirla como el usuario principal
    app.dependency_overrides[get_current_user] = override_get_current_user
    res_share = client.post(f"/api/v1/sessions/{session_id}/share")
    
    assert res_share.status_code == status.HTTP_403_FORBIDDEN