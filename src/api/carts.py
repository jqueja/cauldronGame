from fastapi import APIRouter, Depends, Request, HTTPException, status
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

from ..database import *

router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)

cart_dict = {}

class NewCart(BaseModel):
    customer: str

cart_id = 0

@router.post("/")
def create_cart(new_cart: NewCart):
    """ """
    print("Created new Cart")
    global cart_id

    cart_id += 1
    return {"cart_id": cart_id}

@router.get("/{cart_id}")
def get_cart(cart_id: int):

    global cart_dict

    print(cart_dict)
    
    cart_info = cart_dict[cart_id]
    item_sku = cart_info[0]
    quant_item = cart_info[1]

    result_string = f"{item_sku}: {quant_item}"
    print(result_string)
    
    return result_string

class CartItem(BaseModel):
    quantity: int

@router.post("/{cart_id}/items/{item_sku}")
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):
    
    global cart_dict

    # If the customer already exists, update the value
    if cart_id in cart_dict:
        info = cart_dict[cart_id]
        info[1] = cart_item.quantity
        
    # The customer is new, so make a cart for them
    cart_dict[cart_id] = [item_sku, cart_item.quantity]

    print(cart_dict)
    
    return "OK"

class CartCheckout(BaseModel):
    payment: str

@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):

    print(cart_dict)

    cart_info = cart_dict[cart_id]

    print(cart_info[0])
    print(cart_info[1])
 
    # The cart exists
    if cart_info:
        sku = cart_info[0]
        quantity = cart_info[1]

        # Check if we have enough, if we do sell
        if sku == "RED_POTION":
            cur_red_potions = get_red_potions()

            if quantity > cur_red_potions:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer wants too much, don't have enough to sell Red"
            )

            new_potions = cur_red_potions - quantity
            set_red_potions(new_potions)

            gold_payment = 50 * quantity

            gold_amount = get_gold() + gold_payment
            set_gold(gold_amount)

            return {"total_potions_bought": quantity, "total_gold_paid": gold_payment}
        
        elif sku == "GREEN_POTION":
            cur_green_potions = get_green_potions()

            if quantity > cur_green_potions:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer wants too much, don't have enough to sell Green"
            )

            new_potions = cur_green_potions - quantity
            set_green_potions(new_potions)

            gold_payment = 50 * quantity

            gold_amount = get_gold() + gold_payment
            set_gold(gold_amount)

            return {"total_potions_bought": quantity, "total_gold_paid": gold_payment}
        
        elif sku == "BLUE_POTION":
            cur_blue_potions = get_blue_potions()

            if quantity > cur_blue_potions:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer wants too much, don't have enough to sell Blue"
            )

            new_potions = cur_blue_potions - quantity
            set_blue_potions(new_potions)

            gold_payment = 50 * quantity

            gold_amount = get_gold() + gold_payment
            set_gold(gold_amount)

            return {"total_potions_bought": quantity, "total_gold_paid": gold_payment}

    # Item does not exist, send HTTP Error
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="cart_id does not exist, cart not created"
        )
