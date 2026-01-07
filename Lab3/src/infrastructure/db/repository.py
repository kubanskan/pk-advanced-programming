import uuid
from typing import List, Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from ...domain.cart import Cart
from ...domain.cart_item import CartItem
from ...application.interfaces.cart_repository import ICartRepository
from .models import CartModel, CartItemModel


class SQLAlchemyCartRepository(ICartRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, cart: Cart):
        cart_model = self.session.query(CartModel).filter_by(id=str(cart.id)).first()

        if not cart_model:
            cart_model = CartModel(
                id=str(cart.id),
                user_id=str(cart.user_id),
                last_activity_at=cart.last_activity_at,
                is_checked_out=cart.is_checked_out
            )
            self.session.add(cart_model)
        else:
            cart_model.last_activity_at = cart.last_activity_at
            cart_model.is_checked_out = cart.is_checked_out

        cart_model.items.clear()

        for item in cart.items.values():
            new_item_model = CartItemModel(
                product_id=str(item.product_id),
                quantity=item.quantity
            )
            cart_model.items.append(new_item_model)

        self.session.commit()

    def get_by_id(self, cart_id: uuid.UUID) -> Optional[Cart]:
        cart_model = self.session.query(CartModel).filter_by(id=str(cart_id)).first()

        if not cart_model:
            return None

        cart = Cart(
            user_id=uuid.UUID(cart_model.user_id),
            cart_id=uuid.UUID(cart_model.id)
        )
        cart.last_activity_at = cart_model.last_activity_at
        cart.is_checked_out = cart_model.is_checked_out

        for item_model in cart_model.items:
            p_id = int(item_model.product_id)
            cart.items[p_id] = CartItem(
                product_id=p_id,
                quantity=item_model.quantity
            )

        return cart

    def delete(self, cart_id: uuid.UUID):
        cart_model = self.session.query(CartModel).filter_by(id=str(cart_id)).first()
        if cart_model:
            self.session.delete(cart_model)
            self.session.commit()

    def get_inactive_carts(self, older_than_minutes: int) -> List[Cart]:
        limit_time = datetime.now() - timedelta(minutes=older_than_minutes)

        inactive_models = self.session.query(CartModel).filter(
            CartModel.last_activity_at < limit_time
        ).all()


        results = []
        for model in inactive_models:

            c = Cart(uuid.UUID(model.user_id), uuid.UUID(model.id))
            c.last_activity_at = model.last_activity_at
            results.append(c)

        return results