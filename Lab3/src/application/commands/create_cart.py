from dataclasses import dataclass
from uuid import UUID
from ...domain.cart import Cart
from ..interfaces.cart_repository import ICartRepository


@dataclass
class CreateCartCommand:
    user_id: UUID


class CreateCartHandler:
    def __init__(self, cart_repository: ICartRepository):
        self._repo = cart_repository

    def handle(self, command: CreateCartCommand) -> UUID:
        cart = Cart(user_id=command.user_id)

        self._repo.save(cart)
        return cart.id
