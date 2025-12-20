from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from ..repository.product_history_repository import ProductHistoryRepository
from ..repository.models import ProductHistory, Product
from ..repository.schemas import ProductHistoryResponse


class ProductHistoryService:

    def __init__(self, db: Session):
        self.repository = ProductHistoryRepository(db)

    @staticmethod
    def product_to_dict(product: Product) -> Dict[str, Any]:
        return {
            'id': product.id,
            'name': product.name,
            'category': product.category.value if hasattr(product.category, 'value') else product.category,
            'price': float(product.price),
            'quantity': product.quantity,
            'created_at': product.created_at.isoformat(),
            'updated_at': product.updated_at.isoformat() if product.updated_at else None
        }

    @staticmethod
    def detect_changed_fields(
            previous: Dict[str, Any],
            current: Dict[str, Any]
    ) -> List[str]:
        changed = []
        tracked_fields = ['name', 'category', 'price', 'quantity']

        for field in tracked_fields:
            if previous.get(field) != current.get(field):
                changed.append(field)

        return changed

    def record_update(
            self,
            product: Product,
            previous_state: Dict[str, Any]
    ) -> Optional[ProductHistory]:
        current_state = self.product_to_dict(product)
        changed_fields = self.detect_changed_fields(previous_state, current_state)

        if not changed_fields:
            return None

        changes_desc = []
        for field in changed_fields:
            old_val = previous_state.get(field)
            new_val = current_state.get(field)
            changes_desc.append(f'{field}: {old_val} → {new_val}')

        description = f'Zaktualizowano: {', '.join(changes_desc)}'

        history_entry = ProductHistory(
            product_id=product.id,
            previous_state=previous_state,
            current_state=current_state,
            changed_fields=changed_fields,
        )

        return self.repository.create(history_entry)



    def get_product_history(
            self,
            product_id: int
    ) -> List[ProductHistoryResponse]:
        history = self.repository.get_product_history(product_id)

        return [
            ProductHistoryResponse(
                id=entry.id,
                product_id=entry.product_id,
                previous_state=entry.previous_state,
                current_state=entry.current_state,
                changed_fields=entry.changed_fields,
                changed_at=entry.changed_at.isoformat() if entry.changed_at else None
            )
            for entry in history
        ]
