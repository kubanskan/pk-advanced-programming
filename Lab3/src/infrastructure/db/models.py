from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()

class CartModel(Base):
    __tablename__ = 'carts'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    last_activity_at = Column(DateTime, default=datetime.now)
    is_checked_out = Column(Boolean, default=False)

    items = relationship('CartItemModel', back_populates='cart', cascade='all, delete-orphan')

class CartItemModel(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(String, ForeignKey('carts.id'))
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    cart = relationship('CartModel', back_populates='items')