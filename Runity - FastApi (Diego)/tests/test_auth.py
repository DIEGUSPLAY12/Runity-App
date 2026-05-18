from fastapi.testclient import TestClient
from app.main import app

# Instanciamos el cliente de pruebas
client = TestClient(app)

def test_get_profile_without_token():
    """
    Simula un usuario que intenta acceder a la ruta protegida sin enviar ninguna credencial.
    FastAPI cortará esto con un error 401 Unauthorized.
    """
    response = client.get("/api/v1/profile/")
    
    # Comprobamos que el sistema no le deja pasar (401 No Autorizado)
    assert response.status_code == 401

def test_get_profile_with_invalid_token():
    """
    Simula un usuario que envía una cabecera de Autorización, pero con un token falso.
    Nuestra lógica en get_current_user debe atraparlo y devolver un 401.
    """
    # Creamos una cabecera HTTP con un token inventado
    headers = {"Authorization": "Bearer token_falso_12345"}
    
    response = client.get("/api/v1/profile/", headers=headers)
    
    # Comprobamos que salta nuestro error 401 personalizado
    assert response.status_code == 401
    assert response.json() == {"detail": "Credenciales de acceso inválidas"}