from fastapi import APIRouter, Depends, Request, HTTPException, status
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

from ..database import *
import random


router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)

#cart_dict = {}

class NewCart(BaseModel):
    customer: str

#cart_id = 0


# DONT FORGET TO UPLOAD THE SCEMA SQL

@router.post("/")
def create_cart(new_cart: NewCart):
    with db.engine.begin() as connection:
        result = connection.execute(
        sqlalchemy.text(
            """
            INSERT INTO cart (customer)
            VALUES (:customer)
            RETURNING cart_id;
            """),
        {"customer": new_cart.customer}
        )

    id_call = result.scalar()
    print(id_call)

    return {"cart_id": id_call}
    
@router.get("/{cart_id}")
def get_cart(cart_id: int):
    pass

class CartItem(BaseModel):
    quantity: int

@router.post("/{cart_id}/items/{item_sku}")
def set_item_quantity(cart_id: int, item_sku: str, cart_item: CartItem):

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """
                SELECT cart_id
                FROM cart
                WHERE cart_id = :cart_id
                """
            ),
            {"cart_id": cart_id}
        )

    cart_row_num = result.scalar()
    print(cart_row_num)

    if cart_row_num:
        print("Cart id does EXIST")
        with db.engine.begin() as connection:
            catalog_result = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT id AS catalog_id
                    FROM catalog
                    WHERE sku = :item_sku
                    """
                ),
                {"item_sku": item_sku}
            )
        
        catalog_row_num = catalog_result.scalar()
        print(catalog_row_num)

        if catalog_row_num:
            with db.engine.begin() as connection:
                insert_result = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO cart_items (cart_id, catalog_id, quantity)
                    VALUES (:cart_id, :catalog_id, :quantity)
                    """
                ),
                [{"cart_id": cart_row_num, "catalog_id": catalog_row_num, "quantity": cart_item.quantity}])

        else:
            print("Catalog does NOT EXIST")

    else:
        print("Cart id does NOT EXIST")

    return cart_id
    
class CartCheckout(BaseModel):
    payment: str

@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):

    with db.engine.begin() as connection:
        cart_item_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT cart_id, catalog_id, quantity
                FROM cart_items
                WHERE cart_id = :cart_id
                """
            ),
            {"cart_id": cart_id}
        )

        cart_items = cart_item_result.fetchall()
    
        for item in cart_items:
            cart_id_result = item[0]
            catalog_id_result = item[1]
            quantity_result = item[2]
            print("-----------")
            print(f" cart id: {cart_id_result}")
            print(f" catalog_id: {catalog_id_result}")

            # Truly how much they want
            print(f" quantity: {quantity_result}")

            with db.engine.begin() as connection:
                catalog_result = connection.execute(
                    sqlalchemy.text(
                        """
                        SELECT sku, name, inventory, price
                        FROM catalog
                        WHERE id = :catalog_id
                        """
                    ),
                    {"catalog_id": catalog_id_result}
            )
            # Can use the Cols
            potion = catalog_result.fetchone()
            print(potion)

            print(quantity_result)
            print(potion.inventory)

            # Pick the most you can sell
            quantity_to_sell = min(quantity_result, potion.inventory)
            print(f"Selling this {quantity_to_sell}")

            # You can Buy it! 
            if quantity_to_sell > 0:
                print(f"I am SELLING this: {potion}")
                
                with db.engine.begin() as connection:
                    result = connection.execute(
                    sqlalchemy.text(
                        """
                        UPDATE catalog
                        SET inventory = inventory - :cart_quantity
                        WHERE id = :catalog_id
                        """),
                    [{"catalog_id": catalog_id_result, "cart_quantity": quantity_to_sell}])

                # Updating global inventory
                with db.engine.begin() as connection:
                    result = connection.execute(
                    sqlalchemy.text(
                        """
                        UPDATE global_inventory
                        SET gold = gold + :cart_quantity * :catalog_price
                        """),
                    [{"cart_quantity": quantity_to_sell, "catalog_price": potion.price}])

            else:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Don't have any to sell :( {potion.name}"
            )

                    
    return "ok"

            




'''
@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):

    # Getting data from cart, 
    with db.engine.begin() as connection:
        result = connection.execute(
        sqlalchemy.text(
            """
            SELECT catalog, quantity
            FROM cart
            WHERE id = :cart_id
            """),
        [{"cart_id": cart_id}])

        result_cart = result.fetchall()

        if not result_cart:
            raise HTTPException(status_code=404, detail=f"Cart with ID {cart_id} not found")
        
        row = result_cart[0]
        cart_catalog_id = row.catalog
        cart_quantity = row.quantity


    
    # Grabbing data from the catalog
    with db.engine.begin() as connection:
        result = connection.execute(
        sqlalchemy.text(
            """
            SELECT *
            FROM catalog
            WHERE id = :catalog_id
            """),
        [{"catalog_id": cart_catalog_id}])

        result_catalog = result.fetchall()
        
        row = result_catalog[0]
        catalog_id = row.id
        catalog_price = row.price
        catalog_potion_type = row.potion_type
        catalog_inventory = row.inventory
        catalog_name = row.name

        
        # The customer is asking the right amount, updates catalog
        if cart_quantity <= catalog_inventory:
            print("Inside here")

            with db.engine.begin() as connection:
                result = connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE catalog
                    SET inventory = inventory - :cart_quantity
                    WHERE potion_type = :catalog_potion_type
                    """),
                [{"catalog_potion_type": catalog_potion_type, "cart_quantity": cart_quantity}])

            # Updating global inventory
            with db.engine.begin() as connection:
                result = connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE global_inventory
                    SET gold = gold + :cart_quantity * :catalog_price
                    """),
                [{"cart_quantity": cart_quantity, "catalog_price": catalog_price}])


        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Customer wants too much, don't have enough to sell {catalog_name}"
            )
        
        
    return "ok"
    '''