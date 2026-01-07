from pydantic import BaseModel
from typing import List
from uuid import UUID

class CartItemDTO(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: float
    value: float  # quantity * price

class CartDTO(BaseModel):
    id: UUID
    user_id: UUID
    items: List[CartItemDTO]
    total_value: float