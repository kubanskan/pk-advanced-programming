from dataclasses import dataclass
from uuid import UUID
from ..interfaces.cart_repository import ICartRepository
from ..interfaces.product_service import IProductService
from ..dto.cart_dto import CartDTO, CartItemDTO
from ...domain.exceptions import CartNotFoundException


@dataclass
class GetCartQuery:
    cart_id: UUID


class GetCartHandler:
    def __init__(self, cart_repository: ICartRepository, product_service: IProductService):
        self._repo = cart_repository
        self._product_service = product_service

    def handle(self, query: GetCartQuery) -> CartDTO:
        cart = self._repo.get_by_id(query.cart_id)
        if not cart:
            raise CartNotFoundException(query.cart_id)

        dtos = []
        total_value = 0.0


        for item_id, item in cart.items.items():
            product_info = self._product_service.get_product_info(item_id)


            if product_info:
                name = product_info.get('name', 'Nieznany produkt')
                price = float(product_info.get('price', 0.0))
            else:
                name = 'Produkt niedostępny'
                price = 0.0

            line_value = price * item.quantity
            total_value += line_value

            dtos.append(CartItemDTO(
                product_id=item_id,
                name=name,
                quantity=item.quantity,
                price=price,
                value=line_value
            ))


        return CartDTO(
            id=cart.id,
            user_id=cart.user_id,
            items=dtos,
            total_value=total_value
        )