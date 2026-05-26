import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_current_user

client = TestClient(app)

CURRENT_USER_ID = "12345678-1234-5678-1234-567812345678"
TARGET_USER_ID_1 = "87654321-4321-8765-4321-876543210987"
TARGET_USER_ID_2 = "99999999-9999-9999-9999-999999999999"

def override_get_current_user():
    return CURRENT_USER_ID

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Crea dos perfiles de prueba y limpia relaciones previas."""
    app.dependency_overrides[get_current_user] = lambda: TARGET_USER_ID_1
    client.put("/api/v1/profile/", json={"display_name": "Sugerido 1"})
    
    app.dependency_overrides[get_current_user] = lambda: TARGET_USER_ID_2
    client.put("/api/v1/profile/", json={"display_name": "Sugerido 2"})
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    client.delete(f"/api/v1/friends/{TARGET_USER_ID_1}")
    client.delete(f"/api/v1/friends/{TARGET_USER_ID_2}")

def test_get_suggested_users_success():
    """Comprueba que devuelve usuarios y que nos excluye a nosotros mismos."""
    response = client.get("/api/v1/users/suggested")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert isinstance(data, list)
    assert not any(user["id"] == CURRENT_USER_ID for user in data)
    assert all(user["is_following"] is False for user in data)

def test_suggested_excludes_followed():
    """Comprueba que si empezamos a seguir a alguien, desaparece de sugerencias."""
    # Seguimos al usuario 1
    client.post(f"/api/v1/friends/{TARGET_USER_ID_1}")
    
    response = client.get("/api/v1/users/suggested")
    data = response.json()
    
    # El usuario 1 ya no debe salir
    assert not any(user["id"] == TARGET_USER_ID_1 for user in data)
    # El usuario 2 sí debe seguir saliendo
    assert any(user["id"] == TARGET_USER_ID_2 for user in data)