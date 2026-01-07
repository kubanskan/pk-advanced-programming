from dataclasses import dataclass
from uuid import UUID
from typing import Optional
from ..interfaces.cart_repository import ICartRepository
from ...domain.exceptions import CartNotFoundException


@dataclass
class RemoveItemCommand:
    cart_id: UUID
    product_id: int
    quantity: Optional[int] = None


class RemoveItemHandler:
    def __init__(self, cart_repository: ICartRepository):
        self._repo = cart_repository

    def handle(self, command: RemoveItemCommand):
        cart = self._repo.get_by_id(command.cart_id)
        if not cart:
            raise CartNotFoundException(command.cart_id)

        cart.remove_item(command.product_id, command.quantity)

        self._repo.save(cart)