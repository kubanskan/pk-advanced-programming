from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from .models import ProductCategory


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    category: ProductCategory
    price: float = Field(..., gt=0)  ### ... Ellipsis - to pole nie ma wartości domyślnej i jest wymagane
    quantity: int = Field(..., ge=0)


class ProductListResponse(BaseModel):
    id: int
    name: str


class ProductDetailedResponse(BaseModel):
    id: int
    name: str
    category: ProductCategory
    price: float
    quantity: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class ProductHistoryResponse(BaseModel):
    id: int
    product_id: int
    previous_state: Dict[str, Any]
    current_state: Dict[str, Any]
    changed_fields: List[str]
    changed_at: str


