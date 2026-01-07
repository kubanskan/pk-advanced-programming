from dataclasses import dataclass
from uuid import UUID
from ..interfaces.cart_repository import ICartRepository
from ..interfaces.product_service import IProductService
from ...domain.exceptions import CartNotFoundException, ProductNotFoundException

@dataclass
class AddItemCommand:
    cart_id: UUID
    product_id: int
    quantity: int

class AddItemHandler:
    def __init__(self, cart_repository: ICartRepository, product_service: IProductService):
        self._repo = cart_repository
        self._product_service = product_service

    def handle(self, command: AddItemCommand):

        cart = self._repo.get_by_id(command.cart_id)
        if not cart:
            raise CartNotFoundException(command.cart_id)


        if not self._product_service.exists(command.product_id):
            raise ProductNotFoundException(f'Produkt {command.product_id} nie istnieje.')


        cart.add_item(command.product_id, command.quantity)

        self._repo.save(cart)