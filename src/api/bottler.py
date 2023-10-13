from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

from ..database import *
from ..helper import *


router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)

class PotionInventory(BaseModel):
    potion_type: list[int]
    quantity: int

# Subtract the red mL I have, add red potions

# [0, 0, 0, 0]

# Instead of checking whether or not I can make it into a potion right away.
# What I can do is iterate through the diff indexes and add them together

# Is there a more efficient way to bottle

@router.post("/deliver")
def post_deliver_bottles(potions_delivered: list[PotionInventory]):

    for cur_potion in potions_delivered:

        red_index = cur_potion.potion_type[0]
        green_index = cur_potion.potion_type[1]
        blue_index = cur_potion.potion_type[2]
        dark_index = cur_potion.potion_type[3]

        with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                UPDATE catalog
                SET inventory = inventory + :quantity WHERE potion_type = :potion_type,
                """),
        [{"quantity": cur_potion.quantity, "potion_type": cur_potion.potion_type}])
            
            connection.execute(
            sqlalchemy.text(
                """
                UPDATE global_inventory
                SET num_red_ml = num_red_ml + :red_index,
                    num_green_ml = num_green_ml + :green_index,
                    num_blue_ml = num_blue_ml + :blue_index,
                    num_dark_ml = num_dark_ml + :dark_index
                """),
        [{"red_index": red_index, "green_index": green_index, "blue_index": blue_index, "dark_index": dark_index}])

    return "ok"


# Gets called 4 times a day
# return potions type and quantity
@router.post("/plan")
def get_bottle_plan():
    pass
    """
    Go from barrel to bottle.
    """

    # Each bottle has a quantity of what proportion of red, blue, and
    # green potion to add.
    # Expressed in integers from 1 to 100 that must sum up to 100.

    '''
    cur_red_ml = get_red_ml()
    cur_green_ml = get_green_ml()
    cur_blue_ml = get_blue_ml()
    cur_dark_ml = get_dark_ml()

    with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                SELECT sku, name 
                FROM catalog
                WHERE inventory = 0
                
                """),
        [{}])

    SELECT * FROM potions

    for potion in potions:
        potion.

    return bottle_plan
'''