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

#cart_dict = {}

class NewCart(BaseModel):
    customer: str

#cart_id = 0

@router.post("/")
def create_cart(new_cart: NewCart):
    with db.engine.begin() as connection:
        result = connection.execute(
        sqlalchemy.text(
            """
            INSERT INTO cart
            DEFAULT VALUES
            RETURNING id;
            """)
        )

    id_call = result.scalar()
    print(id_call)

    return id_call
    
@router.get("/{cart_id}")
def get_cart(cart_id: int):
    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT catalog, quantity
                FROM cart
                LEFT JOIN catalog ON cart.id = catalog.id
                WHERE cart.id = :cart_id
                """
            ),
            {"cart_id": cart_id}
        )

        result_cart = result.fetchall()
        
        catalog_id = result_cart[0][0]
        quantity = result_cart[0][1]


    with db.engine.begin() as connection:
        catalog_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT name
                FROM catalog
                WHERE id = :catalog_id
                """
            ),
            {"catalog_id": catalog_id}
        )

        # Gets the potion name
        content = catalog_result.scalar()
        
        return [
            {
            "catalog_name": content,
            "quantity": quantity
            }
        ] 


    

class CartItem(BaseModel):
    quantity: int

@router.post("/{cart_id}/items/{item_sku}")
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):

    with db.engine.begin() as connection:
        result = connection.execute(
        sqlalchemy.text(
            """
            SELECT id
            FROM catalog
            WHERE sku = :item_sku
            """),
        [{"item_sku": item_sku}])
            
        catalog_id = result.scalar()

        if catalog_id is None:
            raise HTTPException(status_code=404, detail=f"Catalog entry with SKU {item_sku} not found")
        
    with db.engine.begin() as connection:
        update_result = connection.execute(
        sqlalchemy.text(
            """
            UPDATE cart
            SET
                catalog = :catalog_id,
                quantity = :quantity
            WHERE
                id = :cart_id
            """),
        [{"quantity": cart_item.quantity, "cart_id": cart_id, "catalog_id": catalog_id}])
        
    return "ok"
    
class CartCheckout(BaseModel):
    payment: str

@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):
    pass

    '''
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
    '''
