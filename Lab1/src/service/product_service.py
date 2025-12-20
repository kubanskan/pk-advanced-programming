from ..repository.schemas import ProductBase
from .product_history_service import ProductHistoryService
from ..repository.product_repository import ProductRepository
from ..repository.forbidden_word_repository import ForbiddenWordRepository
from sqlalchemy.orm import Session
from ..repository.models import Product
from fastapi import HTTPException
from .specification import ProductValidator
from .exceptions import ValidationError


class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.forbidden_word_repository = ForbiddenWordRepository(db)
        self.validator = ProductValidator(self.repository, self.forbidden_word_repository)
        self.history_service = ProductHistoryService(db)

    def save_product(self, product: ProductBase):
        try:
            self.validator.validate(product)
        except ValidationError as e:
            self._raise_http_error(e)

        new_product = Product(
            name=product.name,
            category=product.category,
            price=product.price,
            quantity=product.quantity)

        return self.repository.create(new_product)

    def update_product(self, product_id: int, product: ProductBase):
        existing_product = self.repository.get_by_id(product_id)

        try:
            self.validator.validate(product, product_id)
        except ValidationError as e:
            self._raise_http_error(e)
        previous_state = self.history_service.product_to_dict(existing_product) # inne podejscie do towrzenia obiektu, konstruktor
        existing_product.name = product.name
        existing_product.category = product.category
        existing_product.price = product.price
        existing_product.quantity = product.quantity

        updated_product = self.repository.update(existing_product)
        self.history_service.record_update(updated_product, previous_state)
        return updated_product

    def delete_product(self, product_id: int):
        self.repository.delete(product_id)

    def get_product(self, product_id: int):
        return self.repository.get_by_id(product_id)

    def get_products(self):
        return self.repository.get_all()

    @staticmethod
    def _raise_http_error(error: ValidationError):
        raise HTTPException(status_code=error.status_code, detail=error.message)
