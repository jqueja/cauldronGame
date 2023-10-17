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

        if not result_cart:
            raise HTTPException(status_code=404, detail=f"Cart with ID {cart_id} not found")
        
        row = result_cart[0]
        catalog_id = row.catalog
        quantity = row.quantity

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