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
@router.post("/deliver")
def post_deliver_barrels(barrels_delivered: list[Barrel]):
    """ """

    for i in range(len(barrels_delivered)):
        curGold = getGold()
        curBarrel = barrels_delivered[i]

        # Only buy red barrels
        if curBarrel.sku == "SMALL_RED_BARREL":
            
            if curBarrel.price <= curGold:
                setRedml(getRedml() + curBarrel.ml_per_barrel)
                setGold(getGold() - curBarrel.price)


    return "OK"

# Gets called once a day
# see how much gold and see what I can purchase
# how many small red barrles I can buy
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):

    counter = 0

    for i in range(len(wholesale_catalog)):
        curGold = getGold()
        curBarrel = wholesale_catalog[i]

        # Only buy red barrels
        if curBarrel.sku == "SMALL_RED_BARREL":
            

            if curBarrel.price <= curGold:
                counter += 1


    return [
        {
            "sku": "SMALL_RED_BARREL",
            "quantity": counter,
        }
    ]
