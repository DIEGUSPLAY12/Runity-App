from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from sqlalchemy import desc, asc
from fastapi import HTTPException, status
from typing import List, Literal, Optional
from uuid import UUID
from datetime import datetime, timezone

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.domain import Challenge, ChallengeParticipant
from app.models.domain import Profile
from app.schemas.challenge import ChallengeResponse, ChallengeJoinResponse
from app.schemas.challenge import RankingResponse, RankingEntry, UserRankingContext

router = APIRouter()

@router.get("/", response_model=List[ChallengeResponse])
def get_challenges(
    status: Literal["active", "past", "all"] = Query("active", description="Filtro de estado del reto"),
    sort: Literal["newest", "popular"] = Query("newest", description="Orden de los resultados"),
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """
    Lista los retos disponibles aplicando filtros de estado y orden.
    Calcula dinámicamente el número total de participantes y el progreso del usuario actual.
    """
    now = datetime.now(timezone.utc)

    # 1. Subconsulta para saber cuántos usuarios hay en cada reto
    subq_count = (
        select(
            ChallengeParticipant.challenge_id,
            func.count(ChallengeParticipant.id).label("total_participants")
        )
        .group_by(ChallengeParticipant.challenge_id)
        .subquery()
    )

    # 2. Subconsulta para saber el progreso exacto del usuario que hace la petición
    subq_user_progress = (
        select(
            ChallengeParticipant.challenge_id,
            ChallengeParticipant.score.label("user_score")
        )
        .where(ChallengeParticipant.profile_id == current_user_id)
        .subquery()
    )

    # 3. Construimos la consulta principal uniendo las piezas
    stmt = (
        select(
            Challenge,
            func.coalesce(subq_count.c.total_participants, 0).label("participants_count"),
            subq_user_progress.c.user_score.label("user_progress")
        )
        .outerjoin(subq_count, Challenge.id == subq_count.c.challenge_id)
        .outerjoin(subq_user_progress, Challenge.id == subq_user_progress.c.challenge_id)
    )

    # 4. Aplicamos el filtro de STATUS (El PBI pide que 'active' incluya la fecha actual)
    if status == "active":
        stmt = stmt.where(and_(Challenge.start_date <= now, Challenge.end_date >= now))
    elif status == "past":
        stmt = stmt.where(Challenge.end_date < now)
    # Si es "all", no aplicamos filtro de fecha

    # 5. Aplicamos el ordenamiento (SORT)
    if sort == "popular":
        # Ordenamos por la columna calculada del número de participantes
        stmt = stmt.order_by(func.coalesce(subq_count.c.total_participants, 0).desc())
    else:
        # Por defecto (newest), ordenamos por los más recientes
        stmt = stmt.order_by(Challenge.created_at.desc())

    # 6. Ejecutamos la consulta
    results = db.execute(stmt).all()

    # 7. Formateamos la respuesta para que encaje con Pydantic
    challenges_data = []
    for challenge, p_count, u_progress in results:
        challenge_dict = challenge.__dict__.copy()
        challenge_dict["participants_count"] = p_count
        challenge_dict["user_progress"] = u_progress
        challenges_data.append(challenge_dict)

    return challenges_data

@router.post("/{challenge_id}/join", response_model=ChallengeJoinResponse, status_code=status.HTTP_201_CREATED)
def join_challenge(
    challenge_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """
    Inscribe al usuario actual en un reto específico.
    Aplica validaciones de existencia, periodo activo y doble inscripción.
    """
    # 1. Validación de Existencia
    challenge = db.get(Challenge, challenge_id)
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="El reto no existe."
        )

    # 2. Validación de Periodo Vigente (Regla de negocio)
    now = datetime.now(timezone.utc)
    
    # FIX: Asignar UTC si la base de datos (como SQLite) devuelve una fecha sin zona horaria
    start_date = challenge.start_date.replace(tzinfo=timezone.utc) if challenge.start_date.tzinfo is None else challenge.start_date
    end_date = challenge.end_date.replace(tzinfo=timezone.utc) if challenge.end_date.tzinfo is None else challenge.end_date

    if now < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este reto aún no ha comenzado."
        )
    if now > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Este reto ya ha finalizado."
        )

    # 3. Prevención de Doble Inscripción (Idempotencia)
    existing_participant = db.execute(
        select(ChallengeParticipant).where(
            and_(
                ChallengeParticipant.challenge_id == challenge_id,
                ChallengeParticipant.profile_id == current_user_id
            )
        )
    ).scalar_one_or_none()

    if existing_participant:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Ya estás participando en este reto."
        )

    # 4. Inserción Segura
    try:
        new_participant = ChallengeParticipant(
            challenge_id=challenge_id,
            profile_id=current_user_id,
            score=0 # Inicia con puntuación 0
        )
        db.add(new_participant)
        db.commit()
        
        return {
            "message": "Te has unido al reto con éxito.",
            "challenge_id": challenge_id,
            "score": 0
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al intentar unirse al reto."
        )

@router.get("/{challenge_id}/ranking", response_model=RankingResponse)
def get_challenge_ranking(
    challenge_id: UUID,
    limit: int = Query(10, ge=1, le=100, description="Número de usuarios en el Top N"),
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """
    Devuelve el Top N del ranking de un reto y la posición exacta del usuario actual.
    Usa Window Functions de SQL para calcular la posición real considerando empates.
    """
    # 1. Verificar que el reto existe
    challenge = db.get(Challenge, challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="El reto no existe.")

    # 2. Definimos la Window Function para el cálculo de posiciones
    # Regla: Mayor puntuación primero. En caso de empate, el que se unió antes gana.
    rank_col = func.rank().over(
        order_by=[
            desc(ChallengeParticipant.score), 
            asc(ChallengeParticipant.joined_at)
        ]
    ).label("rank")

    # 3. Construimos la consulta base que genera el ranking completo
    base_query = (
        select(
            rank_col,
            ChallengeParticipant.profile_id,
            Profile.display_name,
            Profile.avatar_url,
            ChallengeParticipant.score,
            ChallengeParticipant.joined_at
        )
        .join(Profile, ChallengeParticipant.profile_id == Profile.id)
        .where(ChallengeParticipant.challenge_id == challenge_id)
        .subquery() 
    )

    # 4. Query 1: Obtener el Top N
    top_n_stmt = select(base_query).order_by(base_query.c.rank).limit(limit)
    top_n_results = db.execute(top_n_stmt).all()

    # Formateamos los resultados del Top N usando nuestro esquema
    top_participants = [
        RankingEntry(
            rank=row.rank,
            profile_id=row.profile_id,
            display_name=row.display_name,
            avatar_url=row.avatar_url,
            score=row.score,
            joined_at=row.joined_at
        )
        for row in top_n_results
    ]

    # 5. Query 2: Obtener la posición del usuario actual
    user_stmt = select(base_query).where(base_query.c.profile_id == current_user_id)
    user_result = db.execute(user_stmt).first()

    # Formateamos el contexto del usuario actual
    if user_result:
        current_user_context = UserRankingContext(
            rank=user_result.rank,
            score=user_result.score,
            is_participating=True
        )
    else:
        current_user_context = UserRankingContext(
            rank=None,
            score=None,
            is_participating=False
        )

    # 6. Devolver el contrato final
    return RankingResponse(
        challenge_id=challenge_id,
        top_participants=top_participants,
        current_user=current_user_context
    )

@router.delete("/{challenge_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
def leave_challenge(
    challenge_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """
    Saca al usuario autenticado de un reto.
    """
    participant = db.execute(
        select(ChallengeParticipant).where(
            and_(
                ChallengeParticipant.challenge_id == challenge_id,
                ChallengeParticipant.profile_id == current_user_id
            )
        )
    ).scalar_one_or_none()

    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No estás inscrito en este reto."
        )

    db.delete(participant)
    db.commit()
    return None