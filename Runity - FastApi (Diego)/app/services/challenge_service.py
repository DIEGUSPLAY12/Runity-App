import uuid
from sqlalchemy.orm import Session as DbSession
from sqlalchemy import select, func
from app.models.domain import Session, Challenge, ChallengeParticipant

def calculate_and_update_score(db: DbSession, participant_id: uuid.UUID) -> int:
    """
    Calcula el score basado en las sesiones del usuario durante el reto.
    Regla: 1 punto por cada 100 metros recorridos.
    """
    participant = db.get(ChallengeParticipant, participant_id)
    if not participant:
        raise ValueError("Participante no encontrado")
        
    challenge = db.get(Challenge, participant.challenge_id)
    if not challenge:
        raise ValueError("Reto no encontrado")

    # Sumar la distancia de las sesiones en el periodo del reto
    stmt = select(func.coalesce(func.sum(Session.distance_meters), 0)).where(
        Session.profile_id == participant.profile_id,
        Session.start_time >= challenge.start_date,
        Session.start_time <= challenge.end_date
    )
    
    total_distance = db.execute(stmt).scalar() or 0

    # Aplicar fórmula: 1 punto por cada 100 metros (división entera)
    new_score = total_distance // 100

    # Actualizar la base de datos solo si el score ha cambiado
    if participant.score != new_score:
        participant.score = new_score
        db.commit()
        db.refresh(participant)

    return participant.score

def get_challenge_ranking(db: DbSession, challenge_id: uuid.UUID, limit: int = 10):
    """
    Obtiene el Top N de un reto aplicando las reglas de desempate determinísticas.
    Orden: Score (Mayor a menor) -> Joined_at (Antigüedad de inscripción, el primero gana)
    """
    stmt = (
        select(ChallengeParticipant)
        .where(ChallengeParticipant.challenge_id == challenge_id)
        .order_by(
            ChallengeParticipant.score.desc(),
            ChallengeParticipant.joined_at.asc()
        )
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()