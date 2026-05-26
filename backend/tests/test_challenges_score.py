import pytest
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, create_engine, event
from sqlalchemy.orm import sessionmaker

# --- PARCHES PARA SQLITE ---
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import JSONB

@compiles(JSONB, 'sqlite')
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "TEXT"
# ---------------------------

from app.core.db import Base
from app.services.challenge_service import calculate_and_update_score
from app.models.domain import Challenge, ChallengeParticipant, Session, Profile

# ==========================================
# FIXTURE DE BASE DE DATOS EN MEMORIA
# ==========================================
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# --- ENSEÑAR A SQLITE QUÉ ES NOW() ---
@event.listens_for(engine, "connect")
def do_connect(dbapi_connection, connection_record):
    # Registra la función now() para que SQLite no explote al leer server_default=text("now()")
    dbapi_connection.create_function("now", 0, lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
# -------------------------------------

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def db():
    """
    Crea una base de datos limpia en memoria para cada test y la destruye al terminar.
    """
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)

# ==========================================
# TESTS
# ==========================================

def test_score_calculation(db):
    # Setup Data
    user_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    
    # Crear un perfil ficticio necesario para las FK
    profile = Profile(id=user_id, display_name="Runner Tester")
    db.add(profile)
    
    challenge = Challenge(
        id=uuid.uuid4(), 
        title="Reto 10K", 
        start_date=now - timedelta(days=2), 
        end_date=now + timedelta(days=5)
    )
    db.add(challenge)
    
    participant = ChallengeParticipant(
        id=uuid.uuid4(), challenge_id=challenge.id, profile_id=user_id, score=0
    )
    db.add(participant)
    db.commit()

    # Añadir sesiones (2 válidas, 1 fuera de fecha)
    db.add(Session(id=uuid.uuid4(), profile_id=user_id, start_time=now, distance_meters=5000, duration_seconds=1800))
    db.add(Session(id=uuid.uuid4(), profile_id=user_id, start_time=now - timedelta(days=1), distance_meters=250, duration_seconds=120))
    db.add(Session(id=uuid.uuid4(), profile_id=user_id, start_time=now - timedelta(days=10), distance_meters=10000, duration_seconds=3600))
    db.commit()

    # Ejecutar lógica
    score = calculate_and_update_score(db, participant.id)

    # Validar: (5000 + 250) / 100 = 52 puntos (la de 10000m se ignora)
    assert score == 52
    assert participant.score == 52


def test_tie_breaker_deterministic_order(db):
    # Setup Data: 3 participantes en el mismo reto
    challenge_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    
    db.add(Challenge(id=challenge_id, title="Desempate", start_date=now - timedelta(days=5), end_date=now + timedelta(days=5)))
    
    # Se unen en distintos momentos, pero con el mismo score (simulado)
    p_a = ChallengeParticipant(id=uuid.uuid4(), challenge_id=challenge_id, profile_id=uuid.uuid4(), score=100, joined_at=now - timedelta(days=3))
    p_b = ChallengeParticipant(id=uuid.uuid4(), challenge_id=challenge_id, profile_id=uuid.uuid4(), score=100, joined_at=now)
    p_c = ChallengeParticipant(id=uuid.uuid4(), challenge_id=challenge_id, profile_id=uuid.uuid4(), score=100, joined_at=now - timedelta(days=1))
    
    # Hacemos el add de perfiles ficticios para que no falle la FK y luego los participantes
    db.add_all([Profile(id=p_a.profile_id), Profile(id=p_b.profile_id), Profile(id=p_c.profile_id)])
    db.add_all([p_a, p_b, p_c])
    db.commit()

    # Simulamos el order_by del ranking
    stmt = select(ChallengeParticipant).where(
        ChallengeParticipant.challenge_id == challenge_id
    ).order_by(
        ChallengeParticipant.score.desc(),
        ChallengeParticipant.joined_at.asc()
    )
    
    ranking = db.execute(stmt).scalars().all()

    # A se unió hace 3 días, C hace 1 día, B hoy.
    assert len(ranking) == 3
    assert ranking[0].id == p_a.id
    assert ranking[1].id == p_c.id
    assert ranking[2].id == p_b.id