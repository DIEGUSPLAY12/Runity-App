import pytest
import uuid
from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.db import Base, get_db
from app.api.deps import get_current_user

# Importamos domain para que Base conozca todas las tablas
import app.models.domain as domain 
from app.models.domain import Challenge, ChallengeParticipant, Profile

# --- FIXES PARA SQLITE ---
@compiles(JSONB, 'sqlite')
def compile_jsonb_sqlite(type_, compiler, **kw):
    return 'TEXT'

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

@event.listens_for(engine, "connect")
def register_sqlite_now(dbapi_connection, connection_record):
    dbapi_connection.create_function("now", 0, lambda: datetime.now(timezone.utc).isoformat())

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- FIXTURES ---
@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def test_user_id():
    return uuid.uuid4()

@pytest.fixture()
def client(db_session, test_user_id):
    def override_get_db():
        yield db_session
    def override_get_current_user():
        return test_user_id

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    # Crear el perfil del usuario actual
    profile = Profile(id=test_user_id, display_name="Yo (Current User)")
    db_session.add(profile)
    db_session.commit()

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

# --- TESTS ---

def test_ranking_order_limit_and_user_context(client, db_session, test_user_id):
    """
    Test 1, 2 y 3: Valida el límite Top N, el orden por puntos, el desempate por fecha
    y comprueba que el contexto del usuario actual se calcula bien.
    """
    challenge_id = uuid.uuid4()
    now_dt = datetime.now(timezone.utc)
    
    db_session.add(Challenge(
        id=challenge_id, title="Reto Épico",
        start_date=now_dt - timedelta(days=1), end_date=now_dt + timedelta(days=5)
    ))

    # Creamos otros 4 usuarios "rivales"
    u1, u2, u3, u4 = uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    db_session.add_all([
        Profile(id=u1, display_name="Rival 1"),
        Profile(id=u2, display_name="Rival 2"),
        Profile(id=u3, display_name="Rival 3"),
        Profile(id=u4, display_name="Rival 4")
    ])

    # Insertamos participaciones simulando distintas situaciones:
    # Rival 1: 150 pts (Será Top 1)
    # Rival 2: 100 pts, se unió hace 5 días (Será Top 2 por desempate)
    # Rival 3: 100 pts, se unió hace 2 días (Será Top 3, pierde el desempate contra Rival 2)
    # Yo (test_user): 50 pts (Seré Top 4)
    # Rival 4: 10 pts (Será Top 5)
    db_session.add_all([
        ChallengeParticipant(id=uuid.uuid4(), challenge_id=challenge_id, profile_id=u1, score=150, joined_at=now_dt),
        ChallengeParticipant(id=uuid.uuid4(), challenge_id=challenge_id, profile_id=u2, score=100, joined_at=now_dt - timedelta(days=5)),
        ChallengeParticipant(id=uuid.uuid4(), challenge_id=challenge_id, profile_id=u3, score=100, joined_at=now_dt - timedelta(days=2)),
        ChallengeParticipant(id=uuid.uuid4(), challenge_id=challenge_id, profile_id=test_user_id, score=50, joined_at=now_dt),
        ChallengeParticipant(id=uuid.uuid4(), challenge_id=challenge_id, profile_id=u4, score=10, joined_at=now_dt),
    ])
    db_session.commit()

    # Pedimos solo el TOP 3
    response = client.get(f"/api/v1/challenges/{challenge_id}/ranking?limit=3")
    assert response.status_code == 200
    data = response.json()

    # Validamos Limit y Order
    assert len(data["top_participants"]) == 3
    assert data["top_participants"][0]["profile_id"] == str(u1) # Top 1
    assert data["top_participants"][1]["profile_id"] == str(u2) # Top 2 (Ganó desempate)
    assert data["top_participants"][2]["profile_id"] == str(u3) # Top 3 (Perdió desempate)

    # Validamos que, aunque pedimos Top 3, a mi me devuelve mi posición (Top 4) en el bloque "current_user"
    assert data["current_user"]["is_participating"] == True
    assert data["current_user"]["rank"] == 4
    assert data["current_user"]["score"] == 50


def test_ranking_user_not_participating(client, db_session, test_user_id):
    """
    Test 4: Si pido el ranking de un reto donde no estoy inscrito, me tiene
    que devolver la lista, pero mi 'current_user' debe salir vacío/false.
    """
    challenge_id = uuid.uuid4()
    now_dt = datetime.now(timezone.utc)
    
    db_session.add(Challenge(
        id=challenge_id, title="Reto al que no me uní",
        start_date=now_dt - timedelta(days=1), end_date=now_dt + timedelta(days=5)
    ))
    db_session.commit()

    response = client.get(f"/api/v1/challenges/{challenge_id}/ranking")
    assert response.status_code == 200
    data = response.json()

    assert data["current_user"]["is_participating"] == False
    assert data["current_user"]["rank"] is None
    assert data["current_user"]["score"] is None


def test_ranking_non_existent_challenge(client):
    """Test 5: Validar error 404 si el reto no existe."""
    fake_id = uuid.uuid4()
    response = client.get(f"/api/v1/challenges/{fake_id}/ranking")
    assert response.status_code == 404