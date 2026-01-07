import uuid
from datetime import datetime
from typing import List, Dict
from .cart_item import CartItem
from .exceptions import EmptyCartException


class Cart:
    def __init__(self, user_id: uuid.UUID, cart_id: uuid.UUID = None):
        self.id = cart_id or uuid.uuid4()
        self.user_id = user_id

        self.items: Dict[uuid.UUID, CartItem] = {}

        self.last_activity_at = datetime.now()
        self.is_checked_out = False

    def add_item(self, product_id: uuid.UUID, quantity: int):
        self._touch()
        if quantity <= 0:
            raise ValueError('Ilość musi być dodatnia.')

        if product_id in self.items:
            self.items[product_id].increase_quantity(quantity)
        else:
            self.items[product_id] = CartItem(product_id=product_id, quantity=quantity)

    def remove_item(self, product_id: uuid.UUID, quantity: int = None):
        '''
        Usuwa produkt lub zmniejsza jego ilość.
        Jeśli quantity is None lub >= aktualna ilość, usuwa całą pozycję.
        '''
        self._touch()
        if product_id not in self.items:
            return

        current_item = self.items[product_id]

        if quantity is None or quantity >= current_item.quantity:
            del self.items[product_id]
        else:
            current_item.decrease_quantity(quantity)

    def checkout(self):
        self._touch()
        if not self.items:
            raise EmptyCartException('Nie można zatwierdzić pustego koszyka.')
        self.is_checked_out = True

    def _touch(self):
        self.last_activity_at = datetime.now()
