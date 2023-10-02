from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

from ..database import *


router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)

class PotionInventory(BaseModel):
    potion_type: list[int]
    quantity: int

# Subtract the red mL I have, add red potions

# What is the quantity used for??
@router.post("/deliver")
def post_deliver_bottles(potions_delivered: list[PotionInventory]):

    for i in range(len(potions_delivered)):

        curRedml = getRedml()
        
        # Red Potion
        if potions_delivered[i].potion_type[0] == 100:

            totalRedml = potions_delivered[i].quantity * 100

            # How much potions can be created
            potionsCreate = totalRedml // 100

            # Amount of how much to take out
            subtractml = potionsCreate * 100

            newml = curRedml - subtractml
            setRedml(newml)

            curPotions = getRedPotions()

            # Take the current amount of potions and add the new ones
            setRedPotions(curPotions + potionsCreate)

    return [
            {
                "potion_type": [100, 0, 0, 0],
                "quantity": potionsCreate,
            }
        ]
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

    curRedml = getRedml()

    # How much potions can be created
    potionsCreate = curRedml // 100


    return [
            {
                "potion_type": [100, 0, 0, 0],
                "quantity": potionsCreate,
            }
        ]


'''
curRedml = getRedml()
    print(f"Red ml before: {curRedml}")
    print(f"potions before: {getRedPotions()}")



    # How much potions can be created
    potionsCreate = curRedml // 100

    # Amount of how much to take out
    subtractml = potionsCreate * 100

    newml = curRedml - subtractml
    setRedml(newml)

    curPotions = getRedPotions()

    # Take the current amount of potions and add the new ones
    setRedPotions(curPotions + potionsCreate)

    print(f"Red ml after: {getRedml()}")
    print(f"potions after: {getRedPotions()}")
'''