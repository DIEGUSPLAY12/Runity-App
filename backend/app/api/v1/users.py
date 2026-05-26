from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session as DbSession
from sqlalchemy import and_, func, desc

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.domain import Profile, Follow
from app.schemas.profile import UserSearchResult

router = APIRouter()

@router.get("/search", response_model=list[UserSearchResult])
def search_users(
    q: str = Query(..., description="Término de búsqueda (case-insensitive)"),
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """
    Busca usuarios por su display_name excluyendo al usuario actual.
    Calcula al vuelo si el usuario actual ya los está siguiendo.
    """
    results = db.query(
        Profile,
        Follow.follower_id.isnot(None).label("is_following")
    ).outerjoin(
        Follow, 
        and_(
            Follow.followed_id == Profile.id, 
            Follow.follower_id == current_user_id
        )
    ).filter(
        Profile.display_name.ilike(f"%{q}%"),
        Profile.id != current_user_id
    ).all()

    search_response = []
    for profile, is_following in results:
        search_response.append({
            "id": str(profile.id),  # <-- AQUI ESTA LA MAGIA: str()
            "display_name": profile.display_name,
            "is_following": is_following
        })

    return search_response

@router.get("/suggested", response_model=list[UserSearchResult])
def get_suggested_users(
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    """
    Devuelve hasta 10 usuarios que el usuario actual NO sigue,
    ordenados por popularidad (número de seguidores).
    """
    # 1. Subconsulta: Obtener los IDs de los usuarios que ya sigo
    followed_subquery = db.query(Follow.followed_id).filter(
        Follow.follower_id == current_user_id
    )

    # 2. Consulta principal: Buscar perfiles que no soy yo y no están en la subconsulta
    results = db.query(
        Profile,
        func.count(Follow.follower_id).label("follower_count")
    ).outerjoin(
        Follow, Follow.followed_id == Profile.id
    ).filter(
        Profile.id != current_user_id,
        Profile.id.notin_(followed_subquery)
    ).group_by(
        Profile.id
    ).order_by(
        desc("follower_count")
    ).limit(10).all()

    # 3. Empaquetar la respuesta
    suggested_response = []
    for profile, _ in results:
        suggested_response.append({
            "id": str(profile.id),
            "display_name": profile.display_name,
            # Si están en esta lista es porque NO los seguimos
            "is_following": False 
        })

    return suggested_response