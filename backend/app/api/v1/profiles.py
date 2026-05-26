from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DbSession
from uuid import UUID

from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.domain import Profile
from app.schemas.profile import ProfileUpdate, ProfileResponse, ProfilePatch

router = APIRouter()

@router.get("/", response_model=ProfileResponse)
def get_profile(
    db: DbSession = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """
    Recupera el perfil del usuario autenticado mediante su ID extraído del JWT.
    """
  
    profile = db.get(Profile, current_user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return profile

@router.put("/", response_model=ProfileResponse)
def update_profile(
    profile_in: ProfileUpdate,
    db: DbSession = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """
    Actualiza o crea (Upsert) el perfil del usuario actual.
    Garantiza que un usuario solo pueda modificar sus propios datos.
    """
    profile = db.get(Profile, current_user_id)
    
    if profile:
        profile.display_name = profile_in.display_name
        profile.weight_kg = profile_in.weight_kg
        profile.goal = profile_in.goal 

    else:
        profile = Profile(
            id=current_user_id,
            display_name=profile_in.display_name,
            weight_kg=profile_in.weight_kg,
            goal=profile_in.goal 
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.patch("/", response_model=ProfileResponse)
def patch_profile(
    profile_in: ProfilePatch,
    db: DbSession = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user)
):
    """
    Actualiza parcialmente el perfil del usuario actual.
    Solo modifica los campos que se envían explícitamente en el body.
    """
    # 1. Buscamos al usuario en la base de datos
    profile = db.get(Profile, current_user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    # 2. La magia del PATCH: extraemos solo los campos que el frontend nos ha enviado
    # exclude_unset=True significa: "ignora los campos que sean None si el usuario no los mandó"
    update_data = profile_in.model_dump(exclude_unset=True)

    # 3. Recorremos el diccionario dinámico y actualizamos el modelo de SQLAlchemy
    for key, value in update_data.items():
        setattr(profile, key, value)

    # 4. Guardamos los cambios
    db.commit()
    db.refresh(profile)
    
    return profile