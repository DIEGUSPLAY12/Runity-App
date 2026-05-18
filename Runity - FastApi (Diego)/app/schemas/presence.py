from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class PresenceStart(BaseModel):
    session_id: UUID

class PresenceResponse(BaseModel):
    user_id: UUID
    status: str
    session_id: Optional[UUID] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)