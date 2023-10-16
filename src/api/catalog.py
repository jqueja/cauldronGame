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
            SELECT sku, name, inventory, price, potion_type
            FROM catalog
            WHERE inventory != 0
            """
        )
    )
    
    potion_catalog = []

    result_lst = result.fetchall()

    for potion in result_lst:

        if len(potion_catalog) == 6:
            break

        potion_catalog.append(
        {
                "sku": potion.sku,
                "name": potion.name,
                "quantity": potion.inventory,
                "price": potion.price,
                "potion_type": potion.potion_type,
        }
    )
        
    return potion_catalog
    