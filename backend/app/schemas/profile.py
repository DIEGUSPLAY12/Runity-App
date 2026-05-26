from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

# Esquema para la validación de entrada (Request Body) en actualizaciones
class ProfileUpdate(BaseModel):
    """
    Define los campos permitidos y sus reglas de validación al editar un perfil.
    """
    display_name: str = Field(..., min_length=2, description="Nombre visible del usuario")
    weight_kg: Optional[float] = Field(None, gt=0, description="Peso en kilogramos (opcional)")
    
    height_cm: Optional[int] = Field(None, gt=0, description="Altura en centímetros (opcional)")
    avatar_url: Optional[str] = Field(None, description="URL de la foto de perfil")
    
    goal: Optional[str] = Field(None, description="Objetivo o meta personal del usuario")

# Esquema para la serialización de salida (Response Body)
class ProfileResponse(BaseModel):
    """
    Define la estructura de datos que se envía al cliente (App Móvil).
    """
    id: UUID
    display_name: str | None = None
    weight_kg: Optional[float] = None
    
    height_cm: Optional[int] = None
    avatar_url: Optional[str] = None
    
    goal: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserSearchResult(BaseModel):
    id: str
    display_name: str | None = None
    is_following: bool

    model_config = ConfigDict(from_attributes=True)
    
class ProfilePatch(BaseModel):
    """
    Define los campos permitidos al editar parcialmente un perfil (PATCH).
    Todos son opcionales porque el usuario puede enviar solo uno.
    """
    display_name: Optional[str] = Field(None, min_length=2, description="Nombre visible del usuario")
    weight_kg: Optional[float] = Field(None, gt=0, description="Peso en kilogramos")
    height_cm: Optional[int] = Field(None, gt=0, description="Altura en centímetros")
    avatar_url: Optional[str] = Field(None, description="URL de la foto de perfil")
    goal: Optional[str] = Field(None, description="Objetivo o meta personal del usuario")