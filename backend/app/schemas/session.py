from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Literal, List
from datetime import datetime
from uuid import UUID

class SessionBase(BaseModel):
    sport: Literal["running", "cycling", "walking"] = Field(default="running", description="Deporte realizado")
    start_time: datetime = Field(..., description="Fecha y hora de inicio de la carrera")
    distance_meters: int = Field(default=0, ge=0, description="Distancia total en metros")
    duration_seconds: int = Field(default=0, ge=0, description="Duración total en segundos")
    calories: Optional[int] = Field(default=None, ge=0, description="Calorías quemadas")

class SessionCreate(SessionBase):
    pass

class SessionResponse(SessionBase):
    id: UUID
    profile_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class PaginatedSessionResponse(BaseModel):
    items: List[SessionResponse]
    total: int
    page: int
    per_page: int