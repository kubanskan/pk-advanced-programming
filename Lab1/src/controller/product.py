from fastapi import APIRouter, Depends, status
from ..service.product_service import ProductService
from ..repository.database import get_db
from sqlalchemy.orm import Session
from typing import List
from ..repository.schemas import ProductDetailedResponse, ProductListResponse, ProductBase, ProductHistoryResponse
from ..service.product_history_service import ProductHistoryService

router = APIRouter(
    prefix='/api/v1/products'
)


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


def get_product_history_service(db: Session = Depends(get_db)) -> ProductHistoryService:
    return ProductHistoryService(db)


@router.get('/', response_model=List[ProductListResponse])
def get_all_products(
        service: ProductService = Depends(get_product_service)
):
    products = service.get_products()
    return products


@router.get('/{product_id}', response_model=ProductDetailedResponse)
def get_product_by_id(
        product_id: int,
        service: ProductService = Depends(get_product_service)
):
    product = service.get_product(product_id)

    return product


@router.post('/', response_model=ProductDetailedResponse, status_code=status.HTTP_201_CREATED)
def create_product(
        product_data: ProductBase,
        service: ProductService = Depends(get_product_service)
):
    new_product = service.save_product(product_data)
    return new_product


@router.put('/{product_id}', response_model=ProductDetailedResponse)
def update_product(
        product_id: int,
        product_data: ProductBase,
        service: ProductService = Depends(get_product_service)
):
    updated_product = service.update_product(product_id, product_data)
    return updated_product


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
        product_id: int,
        service: ProductService = Depends(get_product_service)
):
    # obsługa wyjątku
    success = service.delete_product(product_id)

    return success


@router.get(
    '/{product_id}/history',
    response_model=List[ProductHistoryResponse]
)
def get_product_history(
        product_id: int,
        service: ProductHistoryService = Depends(get_product_history_service)
):
    return service.get_product_history(product_id) or []
