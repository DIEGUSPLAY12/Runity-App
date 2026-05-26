from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session as DbSession
from sqlalchemy.exc import IntegrityError

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.domain import Profile, Follow
from app.models.domain import Notification

router = APIRouter()

@router.get("/")
def get_friends(
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """Devuelve la lista de perfiles a los que sigue el usuario autenticado."""
    friends = db.query(Profile).join(
        Follow, Follow.followed_id == Profile.id
    ).filter(
        Follow.follower_id == current_user_id
    ).all()
    return friends

@router.post("/{user_id}", status_code=status.HTTP_201_CREATED)
def follow_user(
    user_id: str,
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """Crea una relación de seguimiento y genera una notificación."""
    if str(user_id) == str(current_user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes seguirte a ti mismo.")

    target_user = db.query(Profile).filter(Profile.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario que intentas seguir no existe.")

    # 1. Preparamos el registro de seguimiento
    new_follow = Follow(follower_id=current_user_id, followed_id=user_id)
    db.add(new_follow)

    # 2. Preparamos la notificación para el usuario que recibe el follow
    notification = Notification(
        profile_id=user_id,
        type="new_follower",
        title="¡Nuevo seguidor!",
        message="Alguien ha comenzado a seguir tus entrenamientos."
    )
    db.add(notification)

    # 3. Intentamos guardar ambas cosas en la base de datos (Transacción atómica)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # Cambiado a 409 Conflict según el DoD
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya sigues a este usuario.")

    return {"detail": "Usuario seguido correctamente."}

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(
    user_id: str,
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """Elimina una relación de seguimiento."""
    follow_record = db.query(Follow).filter(
        Follow.follower_id == current_user_id,
        Follow.followed_id == user_id
    ).first()

    if not follow_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sigues a este usuario.")

    db.delete(follow_record)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)