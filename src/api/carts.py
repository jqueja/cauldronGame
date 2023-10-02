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
    print("Created new Cart")
    return {"cart_id": new_cart.customer}


@router.get("/{cart_id}")
def get_cart(cart_id: int):

    print(dctCart)
    
    cartInfo = dctCart[cart_id]
    itemSku = cartInfo[0]
    quantItem = cartInfo[1]

    resultString = f"{itemSku}: {quantItem}"
    print(resultString)
    
    #return "ok"
    return resultString

class CartItem(BaseModel):
    quantity: int


# Use a python dct
@router.post("/{cart_id}/items/{item_sku}")
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):


    # If the customer already exists, update the value
    if cart_id in dctCart:
        info = dctCart[cart_id]
        info[1] = cart_item.quantity
        

    print(dctCart)
    # The customer is new, so make a cart for them
    dctCart[cart_id] = [item_sku, cart_item.quantity] 
    print(dctCart)

    return "OK"


class CartCheckout(BaseModel):
    payment: str
    
# gold increases, potions decreate
@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):

    cartInfo = dctCart[cart_id]

    if cartInfo:
        print("It exists")

        # Check if we have enough, if we do sell

        # else: Send HTTP Error (customer wants too much)


    # Item does not exist, send HTTP Error
    else:
        print("Item does not exist")

    return {"total_potions_bought": 1, "total_gold_paid": cart_checkout.payment}
