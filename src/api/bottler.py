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

@router.post("/deliver")
def post_deliver_bottles(potions_delivered: list[PotionInventory]):
    

    print(potions_delivered)

    return "OK"

# Gets called 4 times a day
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
                "quantity": getRedPotions(),
            }
        ]
