from fastapi import APIRouter, Depends, Request, HTTPException, status
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

from ..database import *


# Added the HTTPException and status

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

    global dctCart

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

    
    global dctCart

    # If the customer already exists, update the value
    if cart_id in dctCart:
        info = dctCart[cart_id]
        info[1] = cart_item.quantity
        

    # The customer is new, so make a cart for them
    dctCart[cart_id] = [item_sku, cart_item.quantity]

    print(dctCart)
    
    '''
    print(cart_id)
    print(item_sku)
    print(cart_item.quantity)

    #insertOrder(cart_id, item_sku, cart_item.quantity)
    '''

    return "OK"


class CartCheckout(BaseModel):
    payment: str

# gold increases, potions decreate
#NOTE: Check if you have enough
@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):

    print(dctCart)


    cartInfo = dctCart[cart_id]

    print(cartInfo[0])
    print(cartInfo[1])
 
    # The cart exists
    if cartInfo:
        sku = cartInfo[0]
        quantity = cartInfo[1]

        # Check if we have enough, if we do sell
    
        # Assuming that they want Red Potions
        if sku == "RED_POTION" :

            curRedPotions = getRedPotions()

            if quantity > curRedPotions:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer wants too much, don't have enough to sell"
            )

            newPotions = curRedPotions - quantity
            setRedPotions(newPotions)

            goldPayment = 50 * quantity

            goldAmount = getGold() + goldPayment
            setGold(goldAmount)

            return {"total_potions_bought": quantity, "total_gold_paid": goldPayment}
        
        elif sku == "GREEN_POTION":

            curGreenPotions = getGreenPotions()

            if quantity > curGreenPotions:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer wants too much, don't have enough to sell"
            )

            newPotions = curGreenPotions - quantity
            setGreenPotions(newPotions)

            goldPayment = 50 * quantity

            goldAmount = getGold() + goldPayment
            setGold(goldAmount)

            return {"total_potions_bought": quantity, "total_gold_paid": goldPayment}
        
        elif sku == "BLUE_POTION":

            curBluePotions = getBluePotions()

            if quantity > curBluePotions:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer wants too much, don't have enough to sell"
            )

            newPotions = curGreenPotions - quantity
            setBluePotions(newPotions)

            goldPayment = 50 * quantity

            goldAmount = getGold() + goldPayment
            setGold(goldAmount)

            return {"total_potions_bought": quantity, "total_gold_paid": goldPayment}


    # Item does not exist, send HTTP Error
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="cart_id does not exist, cart not created"
        )
    