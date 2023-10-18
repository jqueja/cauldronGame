from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.api import auth

from ..database import *
from ..helper import *

import heapq


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

    def __lt__(self, other):
        # Define how Barrels should be compared
        # This is just an example, you may want to adjust it based on your requirements
        return self.price < other.price

# Purchase Battels, increase red ml, check if you can purchase the barrels
# Only buy red

@router.post("/deliver")
def post_deliver_barrels(barrels_delivered: list[Barrel]):

    cur_gold = get_gold()
    cur_red_ml = get_red_ml()
    cur_green_ml = get_green_ml()
    cur_blue_ml = get_blue_ml()

    for cur_barrel in barrels_delivered:

        if (cur_red_ml <= 100) and (cur_barrel.price <= cur_gold) and (cur_barrel.potion_type == [1, 0, 0, 0]):
            cur_red_ml += cur_barrel.ml_per_barrel
            cur_gold -= (cur_barrel.price * 1)

        elif (cur_green_ml <= 100) and (cur_barrel.price <= cur_gold) and (cur_barrel.potion_type == [0 ,1, 0, 0]):
            cur_green_ml += cur_barrel.ml_per_barrel
            cur_gold -= (cur_barrel.price * 1)

        elif (cur_blue_ml <= 100) and (cur_barrel.price <= cur_gold) and (cur_barrel.potion_type == [0, 0, 1, 0]):
            cur_blue_ml += cur_barrel.ml_per_barrel
            cur_gold -= (cur_barrel.price * 1)

        elif (cur_dark_ml <= 50) and (cur_barrel.price <= cur_gold) and (cur_barrel.potion_type == [0, 0, 0, 1]):
            cur_dark_ml += cur_barrel.ml_per_barrel
            cur_gold -= (cur_barrel.price * 1)

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE global_inventory SET
                num_red_ml = :red_ml,
                num_green_ml = :green_ml,
                num_blue_ml = :blue_ml,
                num_dark_ml = :dark_ml,
                gold = :gold_paid
                """),
        [{"red_ml": cur_red_ml, "green_ml": cur_green_ml, "blue_ml": cur_blue_ml, "dark_ml": cur_dark_ml, "gold_paid": cur_gold}])

    return "ok"
        
# Gets called once a day
# see how much gold and see what I can purchase
# how many small red barrles I can buy

# Version 2: How much barrels I can buy in general

@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):

    cur_gold = get_gold()
    cur_red_ml = get_red_ml()
    cur_green_ml = get_green_ml()
    cur_blue_ml = get_blue_ml()
    cur_dark_ml = get_dark_ml()

    purchase_plan = []

    for cur_barrel in wholesale_catalog:

        if (cur_red_ml <= 100) and (cur_barrel.price <= cur_gold) and (cur_barrel.potion_type == [1, 0, 0, 0]):
            cur_red_ml += cur_barrel.ml_per_barrel
            cur_gold -= (cur_barrel.price * 1)
            purchase_plan.append(
                {
                    "sku": cur_barrel.sku,
                    "quantity": 1,
                }
            )

        elif (cur_green_ml <= 100) and (cur_barrel.price <= cur_gold) and (cur_barrel.potion_type == [0 ,1, 0, 0]):
            cur_green_ml += cur_barrel.ml_per_barrel
            cur_gold -= (cur_barrel.price * 1)
            purchase_plan.append(
                {
                    "sku": cur_barrel.sku,
                    "quantity": 1,
                }
            )

        elif (cur_blue_ml <= 100) and (cur_barrel.price <= cur_gold) and (cur_barrel.potion_type == [0, 0, 1, 0]):
            cur_blue_ml += cur_barrel.ml_per_barrel
            cur_gold -= (cur_barrel.price * 1)
            purchase_plan.append(
                {
                    "sku": cur_barrel.sku,
                    "quantity": 1,
                }
            )

        elif (cur_dark_ml <= 50) and (cur_barrel.price <= cur_gold) and (cur_barrel.potion_type == [0, 0, 0, 1]):
            cur_dark_ml += cur_barrel.ml_per_barrel
            cur_gold -= (cur_barrel.price * 1)
            purchase_plan.append(
                {
                    "sku": cur_barrel.sku,
                    "quantity": 1,
                }
            )
