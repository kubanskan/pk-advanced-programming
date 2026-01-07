from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from ...domain.cart import Cart


class ICartRepository(ABC):
    @abstractmethod
    def save(self, cart: Cart):
        pass

    @abstractmethod
    def get_by_id(self, cart_id: UUID) -> Optional[Cart]:
        pass

    @abstractmethod
    def delete(self, cart_id: UUID):
        pass

    @abstractmethod
    def get_inactive_carts(self, older_than_minutes: int) -> list[Cart]:
        pass