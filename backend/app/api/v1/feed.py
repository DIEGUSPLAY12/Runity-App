from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session as DbSession
from sqlalchemy import desc, or_, select

from app.models.domain import Activity, Follow 
from app.api.deps import get_current_user
from app.core.db import get_db

router = APIRouter()

@router.get("/")
def get_feed(
    db: DbSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Resultados por página")
):
    """
    Recupera el feed de actividad ordenado por recencia.
    Incluye la actividad propia y la de los usuarios seguidos.
    """
    # 1. Obtenemos los IDs de los usuarios a los que sigue el usuario actual
    followed_users_query = select(Follow.followed_id).where(
        Follow.follower_id == current_user_id
    )

    # 2. Filtramos la actividad: la mía o la de la gente a la que sigo
    query = db.query(Activity).filter(
        or_(
            Activity.user_id == current_user_id,
            Activity.user_id.in_(followed_users_query)
        )
    ).order_by(desc(Activity.created_at)) 

    # 3. Paginación
    total = query.count()
    activities = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        "items": activities,
        "total": total,
        "page": page,
        "per_page": per_page
    }