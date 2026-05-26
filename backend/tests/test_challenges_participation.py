import pytest
import uuid
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.pool import StaticPool  # <--- NUEVO IMPORT

from app.main import app
from app.core.db import Base, get_db
from app.api.deps import get_current_user

# IMPORTANTE: Importamos todo domain para asegurar que Base conozca TODAS las tablas
import app.models.domain as domain 
from app.models.domain import Challenge, ChallengeParticipant, Profile

# --- TRUCO PARA QUE SQLITE ENTIENDA JSONB DE POSTGRES ---
@compiles(JSONB, 'sqlite')
def compile_jsonb_sqlite(type_, compiler, **kw):
    return 'TEXT'

# --- CONFIGURACIÓN DE DB PARA TEST ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Añadimos poolclass=StaticPool para que los hilos de FastAPI vean las tablas
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # <--- ESTA ES LA CLAVE
)

@event.listens_for(engine, "connect")
def register_sqlite_now(dbapi_connection, connection_record):
    dbapi_connection.create_function("now", 0, lambda: datetime.now(timezone.utc).isoformat())

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- FIXTURES ---

@pytest.fixture()
def db_session():
    """Crea una base de datos limpia para cada test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def test_user_id():
    """Genera un UUID fijo para el usuario de pruebas."""
    return uuid.uuid4()

@pytest.fixture()
def client(db_session, test_user_id):
    """
    Simula un cliente HTTP que ya está autenticado.
    Reemplazamos (override) las dependencias de la DB y del JWT.
    """
    def override_get_db():
        yield db_session

    def override_get_current_user():
        return test_user_id

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    # Crear el perfil del usuario para que las Foreign Keys no fallen
    profile = Profile(id=test_user_id, display_name="Test Runner")
    db_session.add(profile)
    db_session.commit()

    with TestClient(app) as c:
        yield c

    # Limpiar overrides al terminar el test
    app.dependency_overrides.clear()

# --- TESTS ---

def test_join_challenge_success(client, db_session, test_user_id):
    """Test 1: Unirse a un reto activo exitosamente (201)."""
    challenge_id = uuid.uuid4()
    now_dt = datetime.now(timezone.utc)
    
    db_session.add(Challenge(
        id=challenge_id, title="Reto Activo",
        start_date=now_dt - timedelta(days=1), end_date=now_dt + timedelta(days=5)
    ))
    db_session.commit()

    # URL actualizada
    response = client.post(f"/api/v1/challenges/{challenge_id}/join")
    assert response.status_code == 201

    # Verificar que el registro existe en la DB
    participant = db_session.query(ChallengeParticipant).filter_by(
        challenge_id=challenge_id, profile_id=test_user_id
    ).first()
    assert participant is not None


def test_join_non_existent_challenge(client):
    """Test 2: Unirse a un reto que no existe (404)."""
    fake_id = uuid.uuid4()
    # URL actualizada
    response = client.post(f"/api/v1/challenges/{fake_id}/join")
    assert response.status_code == 404


def test_join_already_joined_challenge(client, db_session, test_user_id):
    """Test 3: Unirse a un reto en el que ya estás (409 Conflict)."""
    challenge_id = uuid.uuid4()
    now_dt = datetime.now(timezone.utc)
    
    db_session.add(Challenge(
        id=challenge_id, title="Reto Activo",
        start_date=now_dt - timedelta(days=1), end_date=now_dt + timedelta(days=5)
    ))
    
    # Inscribimos al usuario manualmente antes de hacer la petición
    db_session.add(ChallengeParticipant(
        id=uuid.uuid4(), challenge_id=challenge_id, profile_id=test_user_id, score=0
    ))
    db_session.commit()

    # URL actualizada
    response = client.post(f"/api/v1/challenges/{challenge_id}/join")
    assert response.status_code == 409


def test_join_expired_challenge(client, db_session):
    """Test 4: Unirse a un reto cuya fecha de fin ya pasó (400)."""
    challenge_id = uuid.uuid4()
    now_dt = datetime.now(timezone.utc)
    
    # Reto que terminó hace 2 días
    db_session.add(Challenge(
        id=challenge_id, title="Reto Expirado",
        start_date=now_dt - timedelta(days=10), end_date=now_dt - timedelta(days=2)
    ))
    db_session.commit()

    # URL actualizada
    response = client.post(f"/api/v1/challenges/{challenge_id}/join")
    assert response.status_code == 400


def test_leave_challenge_success(client, db_session, test_user_id):
    """Test 5: Salir de un reto exitosamente (204)."""
    challenge_id = uuid.uuid4()
    now_dt = datetime.now(timezone.utc)
    
    db_session.add(Challenge(
        id=challenge_id, title="Reto Activo",
        start_date=now_dt - timedelta(days=1), end_date=now_dt + timedelta(days=5)
    ))
    db_session.add(ChallengeParticipant(
        id=uuid.uuid4(), challenge_id=challenge_id, profile_id=test_user_id, score=0
    ))
    db_session.commit()

    # URL actualizada
    response = client.delete(f"/api/v1/challenges/{challenge_id}/leave")
    assert response.status_code == 204

    # Verificar que se borró el registro en la DB
    participant = db_session.query(ChallengeParticipant).filter_by(
        challenge_id=challenge_id, profile_id=test_user_id
    ).first()
    assert participant is None