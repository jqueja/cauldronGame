from fastapi import APIRouter
import sqlalchemy
from src import database as db

from ..database import *


router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    """
    Each unique item combination must have only a single price.
    """

    # Can return a max of 20 items.

    amountReturn = 0

    redPotions = getRedPotions()

    if redPotions >= 20:
        amountReturn = 20
    
    else:
        amountReturn = redPotions

    return [
            {
                "sku": "RED_POTION",
                "name": "red potion",
                "quantity": amountReturn,
                "price": 50,
                "potion_type": [100, 0, 0, 0],
            }
        ]
