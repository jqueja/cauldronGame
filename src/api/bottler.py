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

@router.post("/deliver")
def post_deliver_bottles(potions_delivered: list[PotionInventory]):

    for i in range(len(potions_delivered)):
        
        # Red Potion
        if potions_delivered[i].potion_type[0] == 100:

            curRedml = getRedml()

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
        
        # Green Potion
        elif potions_delivered[i].potion_type[1] == 100:

            curGreenml = getGreenml()

            totalGreenml = potions_delivered[i].quantity * 100

            # How much potions can be created
            potionsCreate = totalGreenml // 100

            # Amount of how much to take out
            subtractml = potionsCreate * 100

            newml = curGreenml - subtractml
            setGreenml(newml)

            curPotions = getGreenPotions()

            # Take the current amount of potions and add the new ones
            setGreenPotions(curPotions + potionsCreate)

        # Blue Potion
        elif potions_delivered[i].potion_type[2] == 100:

            curBlueml = getBlueml()

            totalBlueml = potions_delivered[i].quantity * 100

            # How much potions can be created
            potionsCreate = totalBlueml // 100

            # Amount of how much to take out
            subtractml = potionsCreate * 100

            newml = curBlueml - subtractml
            setBlueml(newml)

            curPotions = getBluePotions()

            # Take the current amount of potions and add the new ones
            setBluePotions(curPotions + potionsCreate)

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

    curRedml = getRedml()
    curGreenml = getGreenml()
    curBlueml = getBlueml()

    # How much potions can be created
    redCreate = curRedml // 100
    greenCreate = curGreenml // 100
    blueCreate = curBlueml // 100


    return [
            {
                "potion_type": [100, 0, 0, 0],
                "quantity": redCreate,
            },
            {
                "potion_type": [0, 100, 0, 0],
                "quantity": greenCreate,
            },
            {
                "potion_type": [0, 0, 100, 0],
                "quantity": blueCreate,
            },
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