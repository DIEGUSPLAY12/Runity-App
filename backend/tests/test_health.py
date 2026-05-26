from fastapi.testclient import TestClient
from app.main import app

# Creamos un cliente de pruebas a partir de tu aplicación principal
client = TestClient(app)

def test_health_check():
    """
    Verifica que el endpoint de estado de la API funciona correctamente
    y devuelve el mensaje esperado.
    """
    response = client.get("/api/v1/health")
    
    # Comprobamos que el código HTTP es 200 (Éxito)
    assert response.status_code == 200
    
    # Comprobamos que el contenido del JSON es exactamente el esperado
    assert response.json() == {"status": "ok", "message": "Hello Runity"}