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
                setBlueml(getBlueml() + curBarrel.ml_per_barrel)
                setGold(curGold - curBarrel.price)


    return "ok"

# Gets called once a day
# see how much gold and see what I can purchase
# how many small red barrles I can buy

# Version 2: How much barrels I can buy in general

#NOTE: Sort the Barrels buy the cheapest to get the most money
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):


    curGold = getGold()

    redCounter = 0
    greenCounter = 0
    blueCounter = 0

    barrelPlan = []




    for i in range(len(wholesale_catalog)):
        curBarrel = wholesale_catalog[i]

        # Checking Red Barrels
        if curBarrel.sku == "SMALL_RED_BARREL":
            
            if curBarrel.price <= curGold:
                curGold -= curBarrel.price
                redCounter += 1

        # Checking Green 
        elif curBarrel.sku == "SMALL_GREEN_BARREL":

            if curBarrel.price <= curGold:
                curGold -= curBarrel.price
                greenCounter += 1

        # Checking Blue
        elif curBarrel.sku == "SMALL_BLUE_BARREl":

            if curBarrel.price <= curGold:
                curGold -= curBarrel.price
                blueCounter += 1


    if redCounter > 0:
        barrelPlan.append(
            {
                "sku": "SMALL_RED_BARREL",
                "quantity": redCounter,
            }
        )

    elif greenCounter > 0:
        barrelPlan.append(
            {
                "sku": "SMALL_GREEN_BARREL",
                "quantity": greenCounter,
            }
        )

    elif blueCounter > 0:
        barrelPlan.append(
            {
                "sku": "SMALL_BLUE_BARREL",
                "quantity": blueCounter,
            }
        )

    return barrelPlan
