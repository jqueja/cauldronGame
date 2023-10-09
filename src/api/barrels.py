from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

from ..database import *


router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
    dependencies=[Depends(auth.get_api_key)],
)

class Barrel(BaseModel):
    sku: str

    ml_per_barrel: int
    potion_type: list[int]
    price: int

    quantity: int

# Purchase Battels, increase red ml, check if you can purchase the barrels
# Only buy red
'''
'''

'''
NOTE: Can we trust the call? Do we have to check for potion type as well?
'''
@router.post("/deliver")
def post_deliver_barrels(barrels_delivered: list[Barrel]):
    """ """

    for i in range(len(barrels_delivered)):
        curGold = getGold()
        curBarrel = barrels_delivered[i]

        print(curBarrel)

        # Only buy red barrels
        #if curBarrel.sku == "SMALL_RED_BARREL":
        
        # Buy all the barrels we can
        if curBarrel.price <= curGold:

            if curBarrel.sku == "SMALL_RED_BARREL":
                setRedml(getRedml() + curBarrel.ml_per_barrel)
                setGold(curGold - curBarrel.price)

            elif curBarrel.sku == "SMALL_GREEN_BARREL":
                setGreenml(getGreenml() + curBarrel.ml_per_barrel)
                setGold(curGold - curBarrel.price)

            elif  curBarrel.sku == "SMALL_BLUE_BARREL":
                setRedml(getBlueml() + curBarrel.ml_per_barrel)
                setGold(curGold - curBarrel.price)


    return "ok"

# Gets called once a day
# see how much gold and see what I can purchase
# how many small red barrles I can buy

# Version 2: How much barrels I can buy in general
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):

    redCounter = 0
    greenCounter = 0
    blueCounter = 0


    for i in range(len(wholesale_catalog)):
        curGold = getGold()
        curBarrel = wholesale_catalog[i]

        # Checking Red Barrels
        if curBarrel.sku == "SMALL_RED_BARREL":
            
            if curBarrel.price <= curGold:
                redCounter += 1

        # Checking Green 
        elif curBarrel.sku == "SMALL_GREEN_BARREL":
            if curBarrel.price <= curGold:
                greenCounter += 1

        # Checking Blue
        elif curBarrel.sku == "SMALL_BLUE_BARREl":

            if curBarrel.price <= curGold:
                blueCounter += 1

    totalCounter = redCounter + greenCounter + blueCounter

    # We have items to sell! 
    if totalCounter > 0:
        return [
            {
                "sku": "SMALL_RED_BARREL",
                "quantity": redCounter,
            },
            {
                "sku": "SMALL_GREEN_BARREL",
                "quantity": greenCounter,
            },
            {
                "sku": "SMALL_BLUE_BARREL",
                "quantity": blueCounter,
            },
        ]
    
    # We have nothing to sell :(
    else:
        return []
