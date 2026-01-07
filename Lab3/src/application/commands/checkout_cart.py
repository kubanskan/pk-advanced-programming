from dataclasses import dataclass
from uuid import UUID
from ...application.interfaces.cart_repository import ICartRepository
from ...domain.exceptions import CartNotFoundException


@dataclass
class CheckoutCartCommand:
    cart_id: UUID


class CheckoutCartHandler:
    def __init__(self, cart_repository: ICartRepository):
        self._repo = cart_repository

    def handle(self, command: CheckoutCartCommand):
        cart = self._repo.get_by_id(command.cart_id)
        if not cart:
            raise CartNotFoundException(command.cart_id)

        cart.checkout()

        self._repo.save(cart)
