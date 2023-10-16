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

    print(wholesale_catalog)


    curGold = get_gold()

    red_counter = 0
    green_counter = 0
    blue_counter = 0
    dark_counter = 0

    barrelPlan = []


    for i in range(len(wholesale_catalog)):
        cur_barrel = wholesale_catalog[i]

        # Red Barrel
        if cur_barrel.potion_type == [1,0,0,0]:
            print("Red")
            
            if cur_barrel.price <= curGold:
                print("Red Add")
                curGold -= cur_barrel.price
                red_counter += 1

        # Green Barrel
        if cur_barrel.potion_type == [0,1,0,0]:


            if cur_barrel.price <= curGold:
                curGold -= cur_barrel.price
                green_counter += 1

        # Blue Barrel
        if cur_barrel.potion_type == [0,0,1,0]:

            if cur_barrel.price <= curGold:
                curGold -= cur_barrel.price
                blue_counter += 1

        # Dark Barrel
        if cur_barrel.potion_type == [0,0,0,1]:
            print("Dark")

            if cur_barrel.price <= curGold:
                print("Dark Add")
                curGold -= cur_barrel.price
                dark_counter += 1


    if red_counter > 0:
        barrelPlan.append(
            {
                "sku": "SMALL_RED_BARREL",
                "quantity": red_counter,
            }
        )

    if green_counter > 0:
        barrelPlan.append(
            {
                "sku": "SMALL_GREEN_BARREL",
                "quantity": green_counter,
            }
        )

    if blue_counter > 0:
        barrelPlan.append(
            {
                "sku": "SMALL_BLUE_BARREL",
                "quantity": blue_counter,
            }
        )

    if dark_counter > 0:
        print("Why not here")
        barrelPlan.append(
            {
                "sku": "SMALL_DARK_BARREL",
                "quantity": dark_counter,
            }
        )

    
    #print(barrelPlan)

    return barrelPlan

# Barrels, gold o