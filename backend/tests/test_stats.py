import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_current_user
from app.core.db import SessionLocal
# CORRECCIÓN: Importamos también Session para poder borrar datos viejos
from app.models.domain import Profile, Session 

client = TestClient(app)

STATS_USER_ID = "99999999-9999-9999-9999-999999999999"

def override_get_stats_user():
    return STATS_USER_ID

@pytest.fixture(scope="module", autouse=True)
def setup_stats_dataset():
    """
    Prepara la base de datos con un usuario limpio y 3 carreras en fechas específicas.
    """
    db = SessionLocal()
    
    # 1. Inyectamos al usuario
    user = db.query(Profile).filter(Profile.id == STATS_USER_ID).first()
    if not user:
        user = Profile(id=STATS_USER_ID, display_name="Usuario Estadisticas")
        db.add(user)
        db.commit()
        
    # CORRECCIÓN: 2. Borramos las carreras de pruebas anteriores para no duplicar datos
    db.query(Session).filter(Session.profile_id == STATS_USER_ID).delete()
    db.commit()
    db.close()

    # 3. Suplantamos la identidad temporalmente para crear las sesiones
    app.dependency_overrides[get_current_user] = override_get_stats_user

    # Semana 10 de 2026
    client.post("/api/v1/sessions/", json={
        "sport": "running", "start_time": "2026-03-09T10:00:00Z", 
        "distance_meters": 5000, "duration_seconds": 1500
    })
    client.post("/api/v1/sessions/", json={
        "sport": "running", "start_time": "2026-03-11T18:00:00Z", 
        "distance_meters": 10000, "duration_seconds": 3600
    })

    # Semana 11 de 2026
    client.post("/api/v1/sessions/", json={
        "sport": "running", "start_time": "2026-03-16T09:00:00Z", 
        "distance_meters": 5000, "duration_seconds": 1800
    })