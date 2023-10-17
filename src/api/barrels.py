from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

from ..database import *
from ..helper import *


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

    print(barrels_delivered)

    gold_paid = 0
    red_ml = 0
    blue_ml = 0
    green_ml = 0
    dark_ml = 0

    for barrel_delivered in barrels_delivered:
        gold_paid += barrel_delivered.price * barrel_delivered.quantity

        # Red Potion
        if barrel_delivered.potion_type == [1,0,0,0]:
            red_ml += barrel_delivered.ml_per_barrel * barrel_delivered.quantity

        # Green Potion
        elif barrel_delivered.potion_type == [0, 1, 0, 0]:
            green_ml += barrel_delivered.ml_per_barrel * barrel_delivered.quantity

        # Blue Potion
        elif barrel_delivered.potion_type == [0, 0, 1, 0]:
            blue_ml += barrel_delivered.ml_per_barrel * barrel_delivered.quantity

        # Dark Potion
        elif barrel_delivered.potion_type == [0, 0, 0, 1]:
            dark_ml += barrel_delivered.ml_per_barrel * barrel_delivered.quantity

        else:
            raise Exception("Invalid potion type")
        
    print(f"gold_paid: {gold_paid}, red_ml: {red_ml}, blue_ml: {blue_ml}, dark_ml: {dark_ml}")

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE global_inventory SET
                num_red_ml = num_red_ml + :red_ml,
                num_green_ml = num_green_ml + :green_ml,
                num_blue_ml = num_blue_ml + :blue_ml,
                num_dark_ml = num_dark_ml + :dark_ml,
                gold = gold - :gold_paid
                """),
        [{"red_ml": red_ml, "green_ml": green_ml, "blue_ml": blue_ml, "dark_ml": dark_ml, "gold_paid": gold_paid}])

    return "ok"



# Gets called once a day
# see how much gold and see what I can purchase
# how many small red barrles I can buy

# Version 2: How much barrels I can buy in general

#NOTE: Sort the Barrels buy the cheapest to get the most money
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):

    cur_gold = get_gold()
    cur_red_ml = get_red_ml()
    cur_green_ml = get_green_ml()
    cur_blue_ml = get_blue_ml()
    cur_dark_ml = get_dark_ml()

    print(cur_gold)
    print(cur_red_ml)
    print(cur_green_ml)
    print(cur_blue_ml)
    print(cur_dark_ml)

    barrel_plan = []

    for cur_barrel in wholesale_catalog:

        total_price = (cur_barrel.price * cur_barrel.quantity)

        # Red
        if (cur_barrel.potion_type == [1,0,0,0]) and (cur_red_ml <= 300) and (total_price <= cur_gold):

            print("Buying Red")
            print(cur_barrel.sku)

            cur_gold -= total_price
            cur_red_ml += cur_barrel.ml_per_barrel * cur_barrel.quantity

            barrel_plan.append (
                {
                    "sku": cur_barrel.sku,
                    "quantity": cur_barrel.quantity,
                }
            )

        # Green
        elif (cur_barrel.potion_type == [0,1,0,0]) and (cur_green_ml <= 300) and (total_price <= cur_gold):
            print("Buying Green")
            print(cur_barrel.sku)

            cur_gold -= total_price
            cur_green_ml += cur_barrel.ml_per_barrel * cur_barrel.quantity

            barrel_plan.append (
                {
                    "sku": cur_barrel.sku,
                    "quantity": cur_barrel.quantity,
                }
            )

        # Blue
        elif (cur_barrel.potion_type == [0,0,1,0]) and (cur_blue_ml <= 300) and (total_price <= cur_gold):
            print("Buying Blue")
            print(cur_barrel.sku)

            cur_gold -= total_price
            cur_blue_ml += cur_barrel.ml_per_barrel * cur_barrel.quantity

            barrel_plan.append (
                {
                    "sku": cur_barrel.sku,
                    "quantity": cur_barrel.quantity,
                }
            )

        # dark
        elif (cur_barrel.potion_type == [0,0,0,1]) and (cur_dark_ml <= 50) and (total_price <= cur_gold):
            print("Buying dark")
            print(cur_barrel.sku)

            cur_gold -= total_price
            cur_dark_ml += cur_barrel.ml_per_barrel * cur_barrel.quantity

            barrel_plan.append (
                {
                    "sku": cur_barrel.sku,
                    "quantity": cur_barrel.quantity,
                }
            )

    return barrel_plan
