import enum
from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, DateTime, Enum
from .database import Base

class NotificationType(str, enum.Enum):
    EMAIL = 'email'
    PUSH = 'push'

class NotificationStatus(str, enum.Enum):
    PENDING = 'pending'
    QUEUED = 'queued'
    SENT = 'sent'
    FAILED = 'failed'
    CANCELED = 'canceled'

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String, index=True)
    content = Column(String)
    channel = Column(Enum(NotificationType))
    scheduled_time = Column(DateTime, default=datetime.now(UTC))
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING)
    retry_count = Column(Integer, default=0)
    timezone = Column(String, default='UTC')