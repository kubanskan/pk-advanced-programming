import logging
from ...application.interfaces.cart_repository import ICartRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CartCleanupService:
    def __init__(self, repository: ICartRepository):
        self.repo = repository

    def clean_old_carts(self, inactivity_minutes: int = 15):
        '''Metoda wywoływana przez pętlę w main.py'''
        carts_to_remove = self.repo.get_inactive_carts(older_than_minutes=inactivity_minutes)

        if not carts_to_remove:
            return

        logger.info(f'Znaleziono {len(carts_to_remove)} nieaktywnych koszyków do usunięcia.')

        for cart in carts_to_remove:
            self.repo.delete(cart.id)

        logger.info('Czyszczenie zakończone.')