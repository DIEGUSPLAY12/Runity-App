from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session as DbSession
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

# IMPORTANTE: Hemos añadido Profile, Follow y Notification aquí
from app.models.domain import Session, Activity, Profile, Follow, Notification 
from app.schemas.session import SessionCreate, SessionResponse, PaginatedSessionResponse
from app.api.deps import get_current_user
from app.core.db import get_db

router = APIRouter()

# 1. POST: CREAR SESIÓN
@router.post("/", response_model=SessionResponse)
def create_session(
    *,
    db: DbSession = Depends(get_db), 
    session_in: SessionCreate,
    current_user_id: str = Depends(get_current_user)
):
    """
    Registra una nueva carrera para el usuario autenticado, genera un evento en el feed
    y notifica a todos los usuarios que lo siguen.
    """
    # 1. Preparar la sesión
    db_session = Session(
        **session_in.model_dump(),
        profile_id=current_user_id
    )
    
    db.add(db_session)
    db.flush() 
    
    # 2. Preparar el evento de actividad asociado (Feed)
    payload_data = {
        "session_id": str(db_session.id),
        "distance_meters": getattr(db_session, 'distance_meters', 0),
        "duration_seconds": getattr(db_session, 'duration_seconds', 0),
        "sport": getattr(db_session, 'sport', 'running')
    }
    
    new_activity = Activity(
        user_id=current_user_id,
        type="session_completed",
        payload=payload_data
    )
    
    db.add(new_activity)

    # 3. --- NUEVA LÓGICA: Notificar a los amigos (seguidores) ---
    # Recuperamos el perfil para saber el nombre de quien acaba de correr
    profile = db.get(Profile, current_user_id)
    nombre_usuario = profile.display_name if profile and profile.display_name else "Un amigo"
    
    # Buscamos a todos los usuarios que siguen a la persona que corrió
    followers = db.query(Follow).filter(Follow.followed_id == current_user_id).all()
    
    # Creamos una notificación por cada seguidor
    for follow in followers:
        notification = Notification(
            profile_id=follow.follower_id, # La notificación va al seguidor
            type="friend_session_completed",
            title=f"{nombre_usuario} ha completado un entrenamiento",
            message=f"Ha recorrido {db_session.distance_meters} metros en {db_session.duration_seconds // 60} minutos."
        )
        db.add(notification)
    # --------------------------------------------------------------
    
    # 4. Guardar todos los registros de forma atómica (Sesión, Actividad y Notificaciones)
    db.commit()
    db.refresh(db_session)
    
    return db_session

# 2. GET: LISTADO CON PAGINACIÓN Y FILTROS (Tarea 97404)
@router.get("/", response_model=PaginatedSessionResponse)
def read_sessions(
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Resultados por página"),
    sport: Optional[str] = Query(None, description="Filtrar por deporte"),
    date_from: Optional[datetime] = Query(None, description="Fecha de inicio"),
    date_to: Optional[datetime] = Query(None, description="Fecha de fin")
):
    """
    Recupera el historial de sesiones con filtros y paginación.
    """
    query = db.query(Session).filter(Session.profile_id == current_user_id)
    
    if sport:
        query = query.filter(Session.sport == sport)
    if date_from:
        query = query.filter(Session.start_time >= date_from)
    if date_to:
        query = query.filter(Session.start_time <= date_to)
        
    query = query.order_by(desc(Session.start_time))
    
    total = query.count()
    sessions = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "items": sessions,
        "total": total,
        "page": page,
        "per_page": per_page
    }

# 3. GET: DETALLE DE UNA SESIÓN (Tarea 97405)
@router.get("/{session_id}", response_model=SessionResponse)
def read_session_detail(
    session_id: UUID,
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """
    Recupera los detalles de una sesión específica validando que pertenezca al usuario.
    """
    session = db.query(Session).filter(
        Session.id == session_id,
        Session.profile_id == current_user_id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesión no encontrada"
        )
        
    return session

@router.post("/{session_id}/share", status_code=status.HTTP_201_CREATED)
def share_session(
    session_id: str,
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """Comparte una sesión en el muro de actividad del usuario."""
    
    # 1. Buscar la sesión y comprobar que existe
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sesión no encontrada.")

    # 2. Verificar ownership (solo puedes compartir tus propias carreras)
    if str(session.profile_id) != str(current_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes compartir una sesión que no es tuya.")

    # 3. Evitar duplicados (consultando dentro del JSONB)
    existing_activity = db.query(Activity).filter(
        Activity.user_id == current_user_id,
        Activity.type == "session_shared",
        Activity.payload.op('->>')('session_id') == str(session_id)
    ).first()

    if existing_activity:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya has compartido esta sesión en tu muro.")

    # 4. Crear el evento en Activity
    payload_data = {
        "session_id": str(session.id),
        "distance_meters": session.distance_meters,
        "duration_seconds": getattr(session, 'duration_seconds', 0),
        "sport": getattr(session, 'sport', 'running') 
    }

    new_activity = Activity(
        user_id=current_user_id,
        type="session_shared",
        payload=payload_data
    )
    
    db.add(new_activity)
    db.commit()

    return {"detail": "Sesión compartida con éxito en tu muro."}