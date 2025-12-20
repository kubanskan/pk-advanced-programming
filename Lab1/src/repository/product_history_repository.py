from sqlalchemy.orm import Session
from typing import Sequence
from .models import ProductHistory
from sqlalchemy import select


class ProductHistoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, history_entry: ProductHistory) -> ProductHistory:
        self.db.add(history_entry)
        self.db.commit()
        self.db.refresh(history_entry)
        return history_entry

    def get_product_history(
            self,
            product_id: int
    ) -> Sequence[ProductHistory]:
        stmt = (
            select(ProductHistory)
            .where(ProductHistory.product_id == product_id)
            .order_by(ProductHistory.changed_at.desc())
        )
        return self.db.scalars(stmt).all()
