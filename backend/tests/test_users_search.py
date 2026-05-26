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
    # 1. Crear perfil del usuario actual
    client.put("/api/v1/profile/", json={"display_name": "Atleta Principal"})
    
    # 2. Crear perfil del usuario destino con un nombre específico para buscar
    app.dependency_overrides[get_current_user] = lambda: TARGET_USER_ID
    client.put("/api/v1/profile/", json={"display_name": "Corredor Oculto"})
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    # 3. Limpiar follows
    client.delete(f"/api/v1/friends/{TARGET_USER_ID}")

def test_get_friends_list():
    # Seguir al usuario y comprobar que sale en la lista
    client.post(f"/api/v1/friends/{TARGET_USER_ID}")
    response = client.get("/api/v1/friends/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert any(friend["id"] == TARGET_USER_ID for friend in data)

def test_search_users_case_insensitive():
    # Buscar en minúsculas algo que está en mayúsculas
    response = client.get("/api/v1/users/search?q=corredor")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert len(data) > 0
    assert data[0]["display_name"] == "Corredor Oculto"
    assert data[0]["is_following"] == False # Aún no le seguimos

def test_search_users_is_following_flag():
    # Seguir al usuario
    client.post(f"/api/v1/friends/{TARGET_USER_ID}")
    
    # Volver a buscar y comprobar que el flag cambió a True
    response = client.get("/api/v1/users/search?q=Corredor")
    data = response.json()
    assert data[0]["is_following"] == True

def test_search_excludes_self():
    # Buscar una palabra que forma parte de nuestro nombre ("Atleta")
    response = client.get("/api/v1/users/search?q=Atleta")
    data = response.json()
    
    # Comprobamos que nuestro propio ID NO aparece en los resultados
    assert not any(user["id"] == CURRENT_USER_ID for user in data)