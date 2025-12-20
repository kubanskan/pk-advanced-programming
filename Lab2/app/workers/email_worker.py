import time
import random
from datetime import datetime, UTC
from .base_worker import BaseWorker


class EmailWorker(BaseWorker):
    def __init__(self):

        super().__init__(queue_name='email_queue', logger_tag='[EMAIL]')

    def send_logic(self, notification):
        if random.random() < 0.3:
            raise Exception('Przekroczono czas oczekiwania serwera')


        with open('delivery.log', 'a') as f:
            f.write(f'{datetime.now(UTC)} [EMAIL] Wysłano do {notification.recipient}\n')


if __name__ == '__main__':
    time.sleep(10)
    worker = EmailWorker()
    worker.run()
