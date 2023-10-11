from fastapi import APIRouter
import sqlalchemy
from src import database as db

from ..database import *


router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():

    numRedPotions =  getRedPotions()
    numGreenPotions = getGreenPotions()
    numBluePotions = getBluePotions()
    
    potionCatalog = []

    if numRedPotions > 0:
        potionCatalog.append(
            {
                    "sku": "RED_POTION",
                    "name": "red potion",
                    "quantity": numRedPotions,
                    "price": 50,
                    "potion_type": [100, 0, 0, 0],
                }
        )
    
    elif numGreenPotions > 0:
        potionCatalog.append(
            {
                    "sku": "GREEN_POTION",
                    "name": "green potion",
                    "quantity": numGreenPotions,
                    "price": 50,
                    "potion_type": [0, 100, 0, 0],
                }
        )

    elif numBluePotions > 0:
        potionCatalog.append(
            {
                    "sku": "BLUE_POTION",
                    "name": "blue potion",
                    "quantity": numBluePotions,
                    "price": 50,
                    "potion_type": [0, 0, 100, 0],
                }
        )

        
    return potionCatalog
    

