from sqlalchemy.orm import Session
from datetime import datetime
from .models import Notification, NotificationStatus

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, notif_data):
        new_notif = Notification(**notif_data.dict(), status=NotificationStatus.PENDING)
        self.db.add(new_notif)
        self.db.commit()
        self.db.refresh(new_notif)
        return new_notif

    def get_by_id(self, notif_id: int):
        return self.db.query(Notification).filter(Notification.id == notif_id).first()

    def get_pending_due(self, now: datetime, limit: int = 10):
        return self.db.query(Notification).filter(
            Notification.status == NotificationStatus.PENDING,
            Notification.scheduled_time <= now
        ).with_for_update(skip_locked=True).limit(limit).all()

    def update_status(self, notif_id: int, status: NotificationStatus):
        notif = self.get_by_id(notif_id)
        if notif:
            notif.status = status
            self.db.commit()
            self.db.refresh(notif)
        return notif