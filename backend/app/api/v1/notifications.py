from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, desc, func
from typing import List, Optional
from uuid import UUID

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.domain import Notification
from app.schemas.notification import NotificationResponse, NotificationCountResponse

router = APIRouter()

@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    unread: Optional[bool] = Query(None, description="Filtrar por no leídas (true) o leídas (false)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """Obtiene el historial de notificaciones con filtros y paginación."""
    stmt = select(Notification).where(Notification.profile_id == current_user_id)
    
    # Aplicar filtro de lectura si se proporciona
    if unread is True:
        stmt = stmt.where(Notification.is_read == False)
    elif unread is False:
        stmt = stmt.where(Notification.is_read == True)
        
    stmt = stmt.order_by(desc(Notification.created_at)).offset(skip).limit(limit)
    
    return db.execute(stmt).scalars().all()

@router.get("/count", response_model=NotificationCountResponse)
def get_notifications_count(
    unread: bool = Query(True, description="Si es true, cuenta solo las no leídas"),
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """Devuelve el número de notificaciones (útil para el badge de la UI)."""
    stmt = select(func.count(Notification.id)).where(Notification.profile_id == current_user_id)
    
    if unread:
        stmt = stmt.where(Notification.is_read == False)
        
    count = db.execute(stmt).scalar()
    return {"unread_count": count}

@router.put("/{notification_id}/read", status_code=status.HTTP_204_NO_CONTENT)
def mark_notification_as_read(
    notification_id: UUID,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """Marca una notificación como leída."""
    notification = db.get(Notification, notification_id)
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    
    if notification.profile_id != current_user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso")

    notification.is_read = True
    db.commit()
    return None