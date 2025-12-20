import time
import json
from abc import ABC, abstractmethod
from ..repository.database import SessionLocal
from ..repository.models import NotificationStatus
from ..repository.repository import NotificationRepository
from ..dispatcher.queue_client import QueueClient


class BaseWorker(ABC):
    def __init__(self, queue_name: str, logger_tag: str):
        self.queue_name = queue_name
        self.tag = logger_tag
        self.queue_client = QueueClient()

    @abstractmethod
    def send_logic(self, notification):
        pass

    def run(self):
        print(f'{self.tag} Worker uruchomiony na kolejce: {self.queue_name}')
        while True:
            task = self.queue_client.pop_task(self.queue_name)
            if not task:
                continue

            data = json.loads(task[1])
            notif_id = data['id']

            db = SessionLocal()
            repo = NotificationRepository(db)

            try:
                notif = repo.get_by_id(notif_id)
                if not notif or notif.status == NotificationStatus.CANCELED:
                    print(f'{self.tag} Zadanie {notif_id} pominięte (anulowane lub brak rekordu).')
                    continue

                print(f'{self.tag} Przetwarzanie zadania {notif_id} do {notif.recipient}...')
                self.send_logic(notif)
                repo.update_status(notif_id, NotificationStatus.SENT)
                print(f'{self.tag} Zadanie {notif_id} WYSŁANE.')

            except Exception as e:
                print(f'{self.tag} Błąd zadania {notif_id}: {e}')
                if notif and notif.retry_count < 3:
                    notif.retry_count += 1
                    repo.update_status(notif_id, NotificationStatus.PENDING)
                    print(f'{self.tag} Zaplanowano ponowną próbę {notif.retry_count}/3')
                elif notif:
                    repo.update_status(notif_id, NotificationStatus.FAILED)
                    print(f'{self.tag} Zadanie {notif_id} TRWALE NIEUDANE.')
            finally:
                db.close()
