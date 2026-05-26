import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_current_user

client = TestClient(app)

CURRENT_USER_ID = "12345678-1234-5678-1234-567812345678"
TARGET_USER_ID = "87654321-4321-8765-4321-876543210987"

def override_get_current_user():
    return CURRENT_USER_ID

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Prepara la BD con un usuario destino y limpia relaciones."""
    app.dependency_overrides[get_current_user] = lambda: TARGET_USER_ID
    client.put("/api/v1/profile/", json={"display_name": "Usuario Destino"})
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    # Nos aseguramos de limpiar ignorando el 404 si no existía
    client.delete(f"/api/v1/friends/{TARGET_USER_ID}")

# --- LOS 5 TESTS DEL DEFINITION OF DONE ---

def test_follow_exitoso_201():
    response = client.post(f"/api/v1/friends/{TARGET_USER_ID}")
    assert response.status_code == status.HTTP_201_CREATED

def test_doble_follow_409():
    # Primer follow
    client.post(f"/api/v1/friends/{TARGET_USER_ID}")
    # Segundo follow (debe dar conflicto)
    response = client.post(f"/api/v1/friends/{TARGET_USER_ID}")
    assert response.status_code == status.HTTP_409_CONFLICT

def test_unfollow_exitoso_204():
    # Seguir primero
    client.post(f"/api/v1/friends/{TARGET_USER_ID}")
    # Dejar de seguir
    response = client.delete(f"/api/v1/friends/{TARGET_USER_ID}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_unfollow_inexistente_404():
    # Intentar dejar de seguir sin haber seguido antes
    response = client.delete(f"/api/v1/friends/{TARGET_USER_ID}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_seguirse_a_si_mismo_400():
    response = client.post(f"/api/v1/friends/{CURRENT_USER_ID}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST