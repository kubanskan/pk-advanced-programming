from fastapi import Depends
from sqlalchemy.orm import Session
from ..infrastructure.db.database import SessionLocal
from ..infrastructure.db.repository import SQLAlchemyCartRepository
from ..infrastructure.external.http_product_client import HttpProductService
from ..application.interfaces.cart_repository import ICartRepository
from ..application.interfaces.product_service import IProductService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_cart_repository(db: Session = Depends(get_db)) -> ICartRepository:
    return SQLAlchemyCartRepository(db)


def get_product_service() -> IProductService:
    return HttpProductService(product_service_url='http://localhost:8005')
