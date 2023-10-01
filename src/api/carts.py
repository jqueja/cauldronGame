from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)

dctCart = {}

class NewCart(BaseModel):
    customer: str


@router.post("/")
def create_cart(new_cart: NewCart):
    """ """
    return {"cart_id": NewCart.customer}


@router.get("/{cart_id}")
def get_cart(cart_id: int):
    """ """

    return {}


class CartItem(BaseModel):
    quantity: int


# Use a python dct
@router.post("/{cart_id}/items/{item_sku}")
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):


    # If the customer already exists, update the value
    if cart_id in dctCart:
        info = dctCart[cart_id]
        info[1] = cart_item.quantity
        

    # The customer is new, so make a cart for them
    dctCart[cart_id] = [item_sku, cart_item.quantity] 

    return "OK"


class CartCheckout(BaseModel):
    payment: str

@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):
    """ """

    

    return {"total_potions_bought": 1, "total_gold_paid": cart_checkout.payment}
