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


@router.post("/deliver")
def post_deliver_bottles(potions_delivered: list[PotionInventory]):

    for i in range(len(potions_delivered)):

        cur_potion = potions_delivered[i]
        
        red_index = cur_potion.potion_type[0]
        green_index = cur_potion.potion_type[1]
        blue_index = cur_potion.potion_type[2]
        dark_index = cur_potion.potion_type[3]
        
        if red_index != 0:
            
            cur_red_ml = get_red_ml()
            
            total_red_ml = (cur_potion.quantity * red_index)
            print(total_red_ml)

            # Wants to take away to much ml
            if total_red_ml > cur_red_ml:
                break

            # How much potions can be created
            potions_create = (total_red_ml) // 100

            # Amount of how much to take out
            subtract_ml = potions_create * 100

            red_ml_change(-1 * subtract_ml)

            red_potion_change(potions_create)
        
        if green_index != 0:

            cur_green_ml = get_green_ml()
            
            total_green_ml = (cur_potion.quantity * green_index)
            print(total_green_ml)

            # Wants to take away to much ml
            if total_green_ml > cur_green_ml:
                break

            # How much potions can be created
            potions_create = (total_green_ml) // 100

            # Amount of how much to take out
            subtract_ml = potions_create * 100

            green_ml_change(-1 * subtract_ml)

            green_potion_change(potions_create)

        if blue_index != 0:

            cur_blue_ml = get_blue_ml()
            
            total_blue_ml = (cur_potion.quantity * blue_index)
            print(total_blue_ml)

            # Wants to take away to much ml
            if total_blue_ml > cur_blue_ml:
                break

            # How much potions can be created
            potions_create = (total_blue_ml) // 100

            # Amount of how much to take out
            subtract_ml = potions_create * 100

            blue_ml_change(-1 * subtract_ml)

            blue_potion_change(potions_create)

        if dark_index != 0:

            cur_dark_ml = get_dark_ml()
            
            total_dark_ml = (cur_potion.quantity * dark_index)
            print(total_dark_ml)

            # Wants to take away to much ml
            if total_dark_ml > cur_dark_ml:
                break

            # How much potions can be created
            potions_create = (total_dark_ml) // 100

            # Amount of how much to take out
            subtract_ml = potions_create * 100

            dark_ml_change(-1 * subtract_ml)

            dark_potion_change(potions_create)

    return "ok"


# Gets called 4 times a day
# return potions type and quantity
@router.post("/plan")
def get_bottle_plan():
    """
    Go from barrel to bottle.
    """

    # Each bottle has a quantity of what proportion of red, blue, and
    # green potion to add.
    # Expressed in integers from 1 to 100 that must sum up to 100.

    # Initial logic: bottle all barrels into red potions.

    # INCREASED Red Potions
    # DECREASED Red ml

    cur_red_ml = get_red_ml()
    cur_green_ml = get_green_ml()
    cur_blue_ml = get_blue_ml()
    cur_dark_ml = get_dark_ml()

    # How much potions can be created
    red_create = cur_red_ml // 100
    green_create = cur_green_ml // 100
    blue_create = cur_blue_ml // 100
    dark_create = cur_dark_ml // 100

    bottle_plan = []
    
    if red_create > 0:
        bottle_plan.append(
            {
                "potion_type": [100, 0, 0, 0],
                "quantity": red_create,
            }
        )
    
    if green_create > 0:
        bottle_plan.append(
            {
                "potion_type": [0, 100, 0, 0],
                "quantity": green_create,
            },
        )

    if blue_create > 0:
        bottle_plan.append(
            {
                "potion_type": [0, 0, 100, 0],
                "quantity": blue_create,
            }
        )

    if dark_create > 0:
        bottle_plan.append(
            {
                "potion_type": [0, 0, 0, 100],
                "quantity": dark_create,
            }
        )
    
    return bottle_plan
