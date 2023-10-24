from fastapi import APIRouter
import sqlalchemy
from src import database as db

from ..database import *


router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():

    with db.engine.begin() as connection:
        result = connection.execute(
        sqlalchemy.text(
            """
            SELECT c.sku, c.name, c.price, c.potion_type, SUM(p.inventory) AS amount
            FROM catalog c
            JOIN potion_ledger_entries p ON c.id = p.potion_id
            GROUP BY c.sku, c.name, c.price, c.potion_type
            HAVING SUM(p.inventory) != 0
            """
        )
    )

    # Fetch all rows from the result
    potions_with_non_zero_inventory = result.fetchall()
        
    potion_catalog = []


    for potion in potions_with_non_zero_inventory:
        print(potion)

        
        if len(potion_catalog) == 6:
            break

        potion_catalog.append(
        {
                "sku": potion.sku,
                "name": potion.name,
                "quantity": potion.amount,
                "price": potion.price,
                "potion_type": potion.potion_type,
        }
    )

    print(potion_catalog)   
    return potion_catalog
    