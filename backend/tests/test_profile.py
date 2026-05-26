from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_current_user

client = TestClient(app)

# --- 1. PREPARACIÓN: El "truco" para saltar Supabase ---
def override_get_current_user():
    """Simula un usuario autenticado devolviendo un UUID válido."""
    return "12345678-1234-5678-1234-567812345678"

# Le decimos a FastAPI que use nuestra función simulada en lugar de la real
app.dependency_overrides[get_current_user] = override_get_current_user

# --- 2. LOS TESTS ---
def test_put_profile():
    """
    Prueba que un usuario autenticado puede crear/actualizar su perfil.
    """
    # Usamos los campos reales de tu esquema Pydantic / SQLAlchemy
    payload = {
        "display_name": "Atleta Prueba",
        "weight_kg": 75.5,
        "goal": "Terminar mi primera 10K"
    }
    
    response = client.put("/api/v1/profile/", json=payload)
    
    # Verificamos que se guardó correctamente
    assert response.status_code == 200
    data = response.json()
    assert data["display_name"] == "Atleta Prueba"
    assert data["goal"] == "Terminar mi primera 10K"
    assert "id" in data

def test_get_profile():
    """
    Prueba que un usuario autenticado puede recuperar sus datos.
    """
    response = client.get("/api/v1/profile/")
    
    assert response.status_code == 200
    data = response.json()
    # Verificamos que nos devuelve el perfil correcto
    assert data["display_name"] == "Atleta Prueba"