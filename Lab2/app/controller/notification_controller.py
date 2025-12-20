from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..repository.database import get_db
from ..schema.notification import NotificationCreate, NotificationResponse
from ..repository.repository import NotificationRepository
from ..service.notification_service import NotificationService

router = APIRouter(prefix='/api/v1/notifications')

@router.post('/', response_model=NotificationResponse)
def create_notification(data: NotificationCreate, db: Session = Depends(get_db)):
    repo = NotificationRepository(db)
    return repo.create(data)

@router.delete('/{id}')
def cancel_notification(id: int, db: Session = Depends(get_db)):
    service = NotificationService(db)
    service.cancel_notification(id)
    return {'message': 'Powiadomienie anulowane'}

@router.post('/{id}/send-now')
def send_notification_now(id: int, db: Session = Depends(get_db)):
    service = NotificationService(db)
    service.send_now(id)
    return {'message': 'Powiadomienie ustawione do natychmiastowego wysłania'}