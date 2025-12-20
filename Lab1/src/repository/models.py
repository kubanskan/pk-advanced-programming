from .database import Base
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, JSON, ForeignKey
import enum
from sqlalchemy.sql import func


class ProductCategory(enum.Enum):
    ELECTRONICS = 'electronics'
    BOOKS = 'books'
    CLOTHING = 'clothing'


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, nullable=False)
    category = Column(Enum(ProductCategory), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ForbiddenWord(Base):
    __tablename__ = 'forbidden_words'
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductHistory(Base):
    __tablename__ = 'product_history'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    previous_state = Column(JSON, nullable=False)
    current_state = Column(JSON, nullable=False)
    changed_fields = Column(JSON, nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
