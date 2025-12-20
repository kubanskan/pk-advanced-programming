from sqlalchemy.orm import Session
from typing import Optional, Sequence
from .models import Product
from sqlalchemy import select


class ProductRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product) -> Product:
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: Product) -> Product:
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product_id: int) -> None:
        self.db.query(Product).filter(Product.id == product_id).delete()
        self.db.commit()

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_all(self) -> Sequence[Product]:
        return self.db.scalars(select(Product)).all()
