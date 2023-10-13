from fastapi import APIRouter
import sqlalchemy
from src import database as db

from ..database import *


router = APIRouter()


@router.get("/catalog/", tags=["catalog"])
def get_catalog():

    num_red_potions =  get_red_potions()
    num_green_potions = get_green_potions()
    num_blue_potions = get_blue_potions()
    num_dark_potions = get_dark_potions()
    
    potion_catalog = []

    if num_red_potions > 0:
        potion_catalog.append(
            {
                    "sku": "RED_POTION",
                    "name": "red potion",
                    "quantity": num_red_potions,
                    "price": 50,
                    "potion_type": [100, 0, 0, 0],
                }
        )
    
    if num_green_potions > 0:
        potion_catalog.append(
            {
                    "sku": "GREEN_POTION",
                    "name": "green potion",
                    "quantity": num_green_potions,
                    "price": 50,
                    "potion_type": [0, 100, 0, 0],
                }
        )

    if num_blue_potions > 0:
        potion_catalog.append(
            {
                    "sku": "BLUE_POTION",
                    "name": "blue potion",
                    "quantity": num_blue_potions,
                    "price": 50,
                    "potion_type": [0, 0, 100, 0],
                }
        )

    if num_dark_potions > 0:
        potion_catalog.append(
            {
                    "sku": "DARK_POTION",
                    "name": "dark potion",
                    "quantity": num_dark_potions,
                    "price": 50,
                    "potion_type": [0, 0, 0, 100],
                }
        )

        
    return potion_catalog
    