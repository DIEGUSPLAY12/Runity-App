import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_current_user
from app.core.db import get_db
from app.models.domain import Activity

# 1. Creamos el cliente de pruebas
client = TestClient(app)

# Simulamos un ID de usuario para el test
FAKE_USER_ID = "12345678-1234-5678-1234-567812345678"

# "Override" de la dependencia para que no pida token real
def override_get_current_user():
    return FAKE_USER_ID

app.dependency_overrides[get_current_user] = override_get_current_user

def test_create_session_and_activity_generation():
    """Prueba que un usuario puede registrar una carrera y se genera el evento session_completed."""
    payload = {
        "start_time": "2026-03-11T10:00:00Z",
        "distance_meters": 5000,
        "duration_seconds": 1500,
        "calories": 350
    }
    response = client.post("/api/v1/sessions/", json=payload)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["distance_meters"] == 5000
    assert "id" in data
    assert data["profile_id"] == FAKE_USER_ID
    
    session_id = data["id"]

    # Verificamos que se ha creado el evento en la tabla activity
    db = next(get_db())
    activity = db.query(Activity).filter(
        Activity.user_id == FAKE_USER_ID,
        Activity.type == "session_completed",
        Activity.payload.op('->>')('session_id') == session_id
    ).first()

    assert activity is not None, "El evento de actividad no se ha creado en la base de datos."
    assert activity.payload["distance_meters"] == 5000
    assert activity.payload["duration_seconds"] == 1500

def test_create_session_invalid_distance():
    """Prueba que el sistema rechaza distancias negativas (Validación Pydantic)."""
    payload = {
        "start_time": "2026-03-11T10:00:00Z",
        "distance_meters": -100,  # Esto debería fallar
        "duration_seconds": 1500
    }
    response = client.post("/api/v1/sessions/", json=payload)
    
    # 422 es Unprocessable Entity (error de validación de esquema)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_get_sessions():
    """Prueba que el GET devuelve las carreras paginadas."""
    response = client.get("/api/v1/sessions/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data # Buscamos la clave 'items' de la paginación
    assert isinstance(data["items"], list)