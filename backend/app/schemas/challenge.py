from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional

class ChallengeBase(BaseModel):
    title: str
    description: Optional[str] = None
    reward_points: int
    image_url: Optional[str] = None  # <--- AÑADIDO AQUÍ
    start_date: datetime
    end_date: datetime

class ChallengeResponse(ChallengeBase):
    id: UUID
    created_at: datetime
    
    # Campos calculados que pide tu PBI
    participants_count: int = 0
    user_progress: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class ChallengeJoinResponse(BaseModel):
    message: str
    challenge_id: UUID
    score: int

class RankingEntry(BaseModel):
    """Representa a un usuario dentro del ranking."""
    rank: int
    profile_id: UUID
    display_name: str | None = None
    avatar_url: str | None = None
    score: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserRankingContext(BaseModel):
    """Representa la situación específica del usuario que hace la petición."""
    rank: int | None = None
    score: int | None = None
    is_participating: bool

class RankingResponse(BaseModel):
    """Contrato final que devuelve el endpoint."""
    challenge_id: UUID
    top_participants: list[RankingEntry]
    current_user: UserRankingContext