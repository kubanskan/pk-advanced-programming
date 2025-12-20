from pydantic import BaseModel
from datetime import datetime
from ..repository.models import NotificationType, NotificationStatus

class NotificationCreate(BaseModel):
    recipient: str
    content: str
    channel: NotificationType
    scheduled_time: datetime
    timezone: str = 'UTC'

class NotificationResponse(NotificationCreate):
    id: int
    status: NotificationStatus
    retry_count: int

    class Config:
        from_attributes = True