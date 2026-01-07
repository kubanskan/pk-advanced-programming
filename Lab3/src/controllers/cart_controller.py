from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from ..controllers.dependencies import get_cart_repository, get_product_service
from ..application.interfaces.cart_repository import ICartRepository
from ..application.interfaces.product_service import IProductService

from ..application.commands.create_cart import CreateCartCommand, CreateCartHandler
from ..application.commands.add_item import AddItemCommand, AddItemHandler
from ..application.commands.remove_item import RemoveItemCommand, RemoveItemHandler
from ..application.commands.checkout_cart import CheckoutCartCommand, CheckoutCartHandler
from ..application.queries.get_cart import GetCartQuery, GetCartHandler
from ..application.dto.cart_dto import CartDTO

router = APIRouter(prefix='/carts', tags=['carts'])


class CreateCartRequest(BaseModel):
    user_id: UUID


class AddItemRequest(BaseModel):
    product_id: int
    quantity: int


class RemoveItemRequest(BaseModel):
    quantity: Optional[int] = None


@router.post('', status_code=status.HTTP_201_CREATED)
def create_cart(
        request: CreateCartRequest,
        repo: ICartRepository = Depends(get_cart_repository)
):
    command = CreateCartCommand(user_id=request.user_id)
    handler = CreateCartHandler(repo)
    cart_id = handler.handle(command)
    return {'cart_id': cart_id}


@router.get('/{cart_id}', response_model=CartDTO)
def get_cart(
        cart_id: UUID,
        repo: ICartRepository = Depends(get_cart_repository),
        prod_service: IProductService = Depends(get_product_service)
):
    query = GetCartQuery(cart_id=cart_id)
    handler = GetCartHandler(repo, prod_service)
    return handler.handle(query)


@router.post('/{cart_id}/items')
def add_item(
        cart_id: UUID,
        request: AddItemRequest,
        repo: ICartRepository = Depends(get_cart_repository),
        prod_service: IProductService = Depends(get_product_service)
):
    command = AddItemCommand(cart_id=cart_id, product_id=request.product_id, quantity=request.quantity)
    handler = AddItemHandler(repo, prod_service)

    handler.handle(command)
    return {'message': 'Produkt dodany'}


@router.delete('/{cart_id}/items/{product_id}')
def remove_item(
        cart_id: UUID,
        product_id: int,
        quantity: Optional[int] = None,  # Query param: ?quantity=1
        repo: ICartRepository = Depends(get_cart_repository)
):
    command = RemoveItemCommand(cart_id=cart_id, product_id=product_id, quantity=quantity)
    handler = RemoveItemHandler(repo)
    handler.handle(command)
    return {'message': 'Produkt usunięty/zaktualizowany'}


@router.post('/{cart_id}/checkout')
def checkout_cart(
        cart_id: UUID,
        repo: ICartRepository = Depends(get_cart_repository)
):
    command = CheckoutCartCommand(cart_id=cart_id)
    handler = CheckoutCartHandler(repo)
    handler.handle(command)
    return {'message': 'Zamówienie zrealizowane pomyślnie'}
