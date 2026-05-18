import pytest
from fastapi import status
from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app
from app.api.deps import get_current_user

# 1. Creamos el cliente de pruebas global
client = TestClient(app)

# 2. Simulamos el ID de usuario como en los otros tests
FAKE_USER_ID = "12345678-1234-5678-1234-567812345678"

def override_get_current_user():
    return FAKE_USER_ID

app.dependency_overrides[get_current_user] = override_get_current_user


def test_start_and_stop_presence():
    """Test de transición de estado: idle -> training -> idle"""
    
    # 1. Crear una sesión ficticia usando tu endpoint real para poder asignarla al presence
    session_payload = {
        "start_time": "2026-04-14T10:00:00Z",
        "distance_meters": 0,
        "duration_seconds": 0,
        "sport": "running"
    }
    session_resp = client.post("/api/v1/sessions/", json=session_payload)
    
    # Nos aseguramos de que la sesión se creó correctamente
    assert session_resp.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
    session_id = session_resp.json()["id"]

    # 2. Iniciar presencia (Pasa a training)
    start_resp = client.post(
        "/api/v1/presence/start", 
        json={"session_id": session_id}
    )
    assert start_resp.status_code == status.HTTP_200_OK
    data = start_resp.json()
    assert data["status"] == "training"
    assert data["session_id"] == session_id

    # 3. Parar presencia (Pasa a idle)
    stop_resp = client.post("/api/v1/presence/stop")
    assert stop_resp.status_code == status.HTTP_200_OK
    stop_data = stop_resp.json()
    assert stop_data["status"] == "idle"
    assert stop_data["session_id"] is None


def test_start_presence_invalid_session():
    """Prueba que el sistema rechaza iniciar presencia con una sesión falsa."""
    fake_session_id = str(uuid4())
    
    start_resp = client.post(
        "/api/v1/presence/start", 
        json={"session_id": fake_session_id}
    )
    
    # Debería dar un 404 porque esa sesión no existe
    assert start_resp.status_code == status.HTTP_404_NOT_FOUND