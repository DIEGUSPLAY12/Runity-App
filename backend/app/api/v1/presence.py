from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update, func
from uuid import UUID

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.domain import Presence, Session as TrainingSession
from app.schemas.presence import PresenceStart, PresenceResponse

router = APIRouter()

@router.post("/start", response_model=PresenceResponse)
def start_presence(
    data: PresenceStart,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """
    Inicia el estado de entrenamiento de forma atómica.
    Utiliza un UPSERT: Si no existe, lo inserta. Si existe, lo actualiza.
    """
    # 1. Verificar que la sesión existe y pertenece al usuario
    session_exists = db.query(TrainingSession).filter(
        TrainingSession.id == data.session_id,
        TrainingSession.profile_id == current_user_id
    ).first()

    if not session_exists:
        raise HTTPException(status_code=404, detail="Sesión no encontrada o no te pertenece")

    # 2. Operación Atómica (Upsert en PostgreSQL)
    stmt = insert(Presence).values(
        user_id=current_user_id,
        status="training",
        session_id=data.session_id
    ).on_conflict_do_update(
        index_elements=['user_id'], # Resolvemos el conflicto usando la Primary Key
        set_={
            'status': 'training', 
            'session_id': data.session_id, 
            'updated_at': func.now()
        }
    ).returning(Presence)

    result = db.execute(stmt).scalar_one()
    db.commit()
    
    return result

@router.post("/stop", response_model=PresenceResponse)
def stop_presence(
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """
    Finaliza el estado de entrenamiento.
    Limpia el session_id y pasa a estado 'idle'.
    """
    # Operación atómica de actualización
    stmt = update(Presence).where(
        Presence.user_id == current_user_id
    ).values(
        status="idle",
        session_id=None,
        updated_at=func.now()
    ).returning(Presence)

    result = db.execute(stmt).scalar_one_or_none()
    
    # Si por algún motivo pulsa "Stop" pero no tenía registro previo en presence,
    # le creamos el registro base en idle para mantener la consistencia.
    if not result:
        stmt_insert = insert(Presence).values(
            user_id=current_user_id,
            status="idle",
            session_id=None
        ).returning(Presence)
        result = db.execute(stmt_insert).scalar_one()

    db.commit()
    return result