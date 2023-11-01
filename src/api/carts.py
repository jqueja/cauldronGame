from fastapi import APIRouter, Depends, Request, HTTPException, status
from pydantic import BaseModel
from src.api import auth
from enum import Enum

import sqlalchemy
from src import database as db

from ..database import *

import json

router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)

class search_sort_options(str, Enum):
    customer_name = "customer_name"
    item_sku = "item_sku"
    line_item_total = "line_item_total"
    timestamp = "timestamp"

class search_sort_order(str, Enum):
    asc = "asc"
    desc = "desc"   

@router.get("/search/", tags=["search"])
def search_orders(
    customer_name: str = "",
    potion_sku: str = "",
    search_page: str = "",
    sort_col: search_sort_options = search_sort_options.timestamp,
    sort_order: search_sort_order = search_sort_order.desc,
):
    """
    Search for cart line items by customer name and/or potion sku.

    Customer name and potion sku filter to orders that contain the 
    string (case insensitive). If the filters aren't provided, no
    filtering occurs on the respective search term.

    Search page is a cursor for pagination. The response to this
    search endpoint will return previous or next if there is a
    previous or next page of results available. The token passed
    in that search response can be passed in the next search request
    as search page to get that page of results.

    Sort col is which column to sort by and sort order is the direction
    of the search. They default to searching by timestamp of the order
    in descending order.

    The response itself contains a previous and next page token (if
    such pages exist) and the results as an array of line items. Each
    line item contains the line item id (must be unique), item sku, 
    customer name, line item total (in gold), and timestamp of the order.
    Your results must be paginated, the max results you can return at any
    time is 5 total line items.
    """

    page_size = 5

    # Determine the offset based on the search_page token

    if search_page == "":
        offset = 0

    else:
        offset = int(search_page)



    # Not negative
    if offset - 5 >= 0:
        prev_page = str(offset - 5)

    else:
        prev_page = ""


    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                f"""
                SELECT
                cart.cart_id AS id,
                cart.customer AS customer_name,
                catalog.name AS purchased_item,
                cart_items.quantity AS quantity,
                cart_items.time AS purchase_time,
                (catalog.price * cart_items.quantity) AS gold,
                cart_items.checked_out AS checked_out
                FROM
                cart
                JOIN
                cart_items ON cart.cart_id = cart_items.cart_id
                JOIN
                catalog ON cart_items.catalog_id = catalog.id
                WHERE
                cart_items.checked_out = True
                AND cart.customer ILIKE '%{customer_name}%'
                AND catalog.name ILIKE '%{potion_sku}%'
                LIMIT {page_size}
                OFFSET {offset};
                """
            )
        )

        # ORDER BY order_by order

    # Fetch all rows from the result
    data = result.fetchall()
    lst = []

    print(data)
    print(len(data))

    # Not negative
    if offset + 5 > len(data):
        next_page = ""

    else:
        next_page = str(offset + 5)


    for row in data:
        sku_string = f"{row.quantity} {row.purchased_item}"

        print(row.id)

        print(sku_string)
        print(row.customer_name)
        print(row.gold)
        print(row.purchase_time)

        lst.append(
            {
                    "line_item_id": row.id,
                    "item_sku": sku_string,
                    "customer_name": row.customer_name,
                    "line_item_total": row.gold,
                    "timestamp": row.purchase_time,
            }
        )

    return {
        "previous": prev_page,
        "next": next_page,
        "results": lst
    }

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

    print("Calling check out")

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

        print(cart_items)
    
        for item in cart_items:
            cart_id_result = item[0]
            catalog_id_result = item[1]
            quantity_result = item[2]
            print("-----------")
            print(f" cart id: {cart_id_result}")
            # What type of potion
            print(f" catalog_id: {catalog_id_result}")

            # Truly how much they want
            print(f" quantity: {quantity_result}")



            with db.engine.begin() as connection:
                catalog_result = connection.execute(
                    sqlalchemy.text(
                        """
                        SELECT sku, name, price, potion_type
                        FROM catalog
                        WHERE id = :catalog_id
                        """
                    ),
                    {"catalog_id": catalog_id_result}
            )

            with db.engine.begin() as connection:
                sum_dark_result = connection.execute(
                    sqlalchemy.text(
                        """
                        SELECT SUM(inventory) AS amount
                        FROM potion_ledger_entries
                        WHERE potion_id = :catalog_id
                        """
                    ),
                    {"catalog_id": catalog_id_result}
                )
                potion_sum_total = sum_dark_result.scalar()

                if potion_sum_total == None:
                    potion_sum_total = 0

            # Can use the Cols
            potion = catalog_result.fetchone()
            print(potion)
            
            # Pick the most you can sell
            quantity_to_sell = min(quantity_result, potion_sum_total)
            
            print(quantity_result)
            print(potion_sum_total)
            print(f"Selling this {quantity_to_sell}")

            # You can Buy it! 
            if quantity_to_sell > 0:

                gold_gain = quantity_to_sell * potion.price

                print(f"I am SELLING this: {potion}")
                
                '''
                # Updating the inventory of the potion
                with db.engine.begin() as connection:
                    result = connection.execute(
                    sqlalchemy.text(
                        """
                        UPDATE catalog
                        SET inventory = inventory - :quantity_to_sell
                        WHERE id = :catalog_id
                        """),
                    [{"catalog_id": catalog_id_result, "quantity_to_sell": quantity_to_sell}])

                
                # Updating global inventory - gold
                with db.engine.begin() as connection:
                    result = connection.execute(
                    sqlalchemy.text(
                        """
                        UPDATE global_inventory
                        SET gold = gold + :cart_quantity * :catalog_price
                        """),
                    [{"cart_quantity": quantity_to_sell, "catalog_price": potion.price}])
                '''


                # Potion Transaction - id
                with db.engine.begin() as connection:
                    description = f"Selling this potion {potion.name}"
                    potion_result = connection.execute(
                        sqlalchemy.text(
                            """
                            INSERT INTO potion_transactions (description)
                            VALUES (:description)
                            RETURNING id;
                            """
                        ),
                        {"description": description}
                    )
                    potions_transaction_id = potion_result.scalar()

                # Catalog id
                with db.engine.begin() as connection:
                    cur_potion_result = connection.execute(
                        sqlalchemy.text(
                            """
                            SELECT id
                            FROM catalog
                            WHERE potion_type = :cur_potion_type;
                            """
                        ),
                        {"cur_potion_type": potion.potion_type}
                    )
                    cur_potion_id = cur_potion_result.scalar()  

                # Ledger this into our db
                with db.engine.begin() as connection:
                    catalog_result = connection.execute(
                        sqlalchemy.text(
                            """
                            INSERT INTO potion_ledger_entries (potion_id, potion_transactions_id, inventory)
                            VALUES (:potion_id, :potion_transactions_id, :potion_sell)
                            """
                        ),
                        [{"potion_id": cur_potion_id, "potion_transactions_id": potions_transaction_id, "potion_sell": quantity_to_sell * -1}])


                # Updating Gain on Gold
                with db.engine.begin() as connection:
                    description = f"Selling this potion: {potion.name} for {gold_gain}"
                    catalog_result = connection.execute(
                        sqlalchemy.text(
                            """
                            INSERT INTO gold_transactions (description)
                            VALUES (:description)
                            RETURNING id;
                            """
                        ),
                        {"description": description}
                    )
                    gold_action_id = catalog_result.scalar()

                
                with db.engine.begin() as connection:
                        catalog_result = connection.execute(
                            sqlalchemy.text(
                                """
                                INSERT INTO gold_ledger_entries (gold_transactions_id, change)
                                VALUES (:gold_action_id, :change)
                                """
                            ),
                            {"gold_action_id": gold_action_id, "change":gold_gain})
                
                # Update the boolean
                with db.engine.begin() as connection:
                    cart_item_result = connection.execute(
                        sqlalchemy.text(
                            """
                            UPDATE cart_items
                            SET checked_out = :checked_out
                            WHERE cart_id = :cart_id
                            """
                        ),
                        {"checked_out": True, "cart_id": cart_id}
                    )

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