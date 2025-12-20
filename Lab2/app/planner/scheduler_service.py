import time
from datetime import datetime, UTC
from ..repository.database import SessionLocal
from ..repository.repository import NotificationRepository
from ..dispatcher.queue_client import QueueClient
from ..repository.models import NotificationStatus


def run_scheduler():
    queue_client = QueueClient()
    print('Planer powiadomień uruchomiony')

    while True:
        db = SessionLocal()
        repo = NotificationRepository(db)
        try:
            tasks = repo.get_pending_due(datetime.now(UTC))

            for task in tasks:
                print(f'Planning task {task.id} -> {task.channel}')

                task.status = NotificationStatus.QUEUED
                db.commit()

                payload = {'id': task.id, 'content': task.content, 'recipient': task.recipient}
                queue_name = f'{task.channel.value}_queue'
                queue_client.push_task(queue_name, payload)

        except Exception as e:
            print(f'Błąd plannera: {e}')
            db.rollback()
        finally:
            db.close()

        time.sleep(2)


if __name__ == '__main__':
    time.sleep(10)
    run_scheduler()