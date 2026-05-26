from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class NotificationResponse(BaseModel):
    id: UUID
    profile_id: UUID
    type: str
    title: str
    message: Optional[str] = None
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NotificationCountResponse(BaseModel):
    unread_count: int