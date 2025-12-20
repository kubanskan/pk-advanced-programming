from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..repository.repository import NotificationRepository
from ..repository.models import NotificationStatus
from datetime import datetime, UTC


class NotificationService:
    def __init__(self, db: Session):
        self.repo = NotificationRepository(db)

    def cancel_notification(self, notif_id: int):
        notif = self.repo.get_by_id(notif_id)
        if not notif:
            raise HTTPException(status_code=404, detail='Powiadomienie nie znalezione')

        if notif.status == NotificationStatus.SENT:
            raise HTTPException(status_code=400, detail='Powiadomienie zostało już wysłane')

        return self.repo.update_status(notif_id, NotificationStatus.CANCELED)

    def send_now(self, notif_id: int):
        notif = self.repo.get_by_id(notif_id)
        if not notif:
            raise HTTPException(status_code=404, detail='Powiadomienie nie znalezione')

        notif.scheduled_time = datetime.now(UTC)
        notif.status = NotificationStatus.PENDING
        self.repo.db.commit()
        return notif