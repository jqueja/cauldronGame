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
    cur_dark_ml = get_dark_ml()

    print(f" Gold: {cur_gold}")
    print(f" Red: {cur_red_ml}")
    print(f" Green: {cur_green_ml}")
    print(f" Blue: {cur_blue_ml}")
    print(f" Dark {cur_dark_ml}")

    barrel_queue = []

    for cur_barrel in barrels_delivered:
        # Calculate the need priority dynamically based on the current quantities
        need_priority = 0
        if cur_barrel.potion_type == [1, 0, 0, 0]:
            need_priority = cur_red_ml
        elif cur_barrel.potion_type == [0, 1, 0, 0]:
            need_priority = cur_green_ml
        elif cur_barrel.potion_type == [0, 0, 1, 0]:
            need_priority = cur_blue_ml
        elif cur_barrel.potion_type == [0, 0, 0, 1]:
            need_priority = cur_dark_ml

        # Use a tuple with need_priority, lower price, and barrel object as the key
        barrel_entry = (need_priority, cur_barrel.price, cur_barrel)
        heapq.heappush(barrel_queue, barrel_entry)

    barrel_plan = []

    while barrel_queue:
        # Pop the barrel with the highest priority
        pop_result = heapq.heappop(barrel_queue)
        cur_barrel = pop_result[2]

        max_quantity_affordable = cur_gold // cur_barrel.price
        quantity_to_buy = min(max_quantity_affordable, cur_barrel.quantity)

        total_price = (cur_barrel.price * quantity_to_buy)

        if total_price <= cur_gold:
            print(f"Buying {cur_barrel.potion_type} - {cur_barrel.sku}")
            print(f"Price: {total_price}")
            print(f"ml in barrel: {quantity_to_buy * cur_barrel.ml_per_barrel}")

            cur_gold -= total_price

            if cur_barrel.potion_type == [1, 0, 0, 0]:
                cur_red_ml += cur_barrel.ml_per_barrel * quantity_to_buy
            elif cur_barrel.potion_type == [0, 1, 0, 0]:
                cur_green_ml += cur_barrel.ml_per_barrel * quantity_to_buy
            elif cur_barrel.potion_type == [0, 0, 1, 0]:
                cur_blue_ml += cur_barrel.ml_per_barrel * quantity_to_buy
            elif cur_barrel.potion_type == [0, 0, 0, 1]:
                cur_dark_ml += cur_barrel.ml_per_barrel * quantity_to_buy

            barrel_plan.append(
                {
                    "sku": cur_barrel.sku,
                    "quantity": cur_barrel.quantity,
                }
            )

    print(f" Gold: {cur_gold}")
    print(f" Red: {cur_red_ml}")
    print(f" Green: {cur_green_ml}")
    print(f" Blue: {cur_blue_ml}")
    print(f" Dark {cur_dark_ml}")

    print(barrel_plan)

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

    print("/plan barrels")

    cur_gold = get_gold()
    cur_red_ml = get_red_ml()
    cur_green_ml = get_green_ml()
    cur_blue_ml = get_blue_ml()
    cur_dark_ml = get_dark_ml()

    print(f" Gold: {cur_gold}")
    print(f" Red: {cur_red_ml}")
    print(f" Green: {cur_green_ml}")
    print(f" Blue: {cur_blue_ml}")
    print(f" Dark {cur_dark_ml}")

    barrel_queue = []

    for cur_barrel in wholesale_catalog:
        # Calculate the need priority dynamically based on current quantities
        need_priority = 0
        if cur_barrel.potion_type == [1, 0, 0, 0]:
            need_priority = -cur_red_ml  
        elif cur_barrel.potion_type == [0, 1, 0, 0]:
            need_priority = -cur_green_ml  
        elif cur_barrel.potion_type == [0, 0, 1, 0]:
            need_priority = -cur_blue_ml  
        elif cur_barrel.potion_type == [0, 0, 0, 1]:
            need_priority = -cur_dark_ml  

        # Use a tuple with need_priority, lower price, and barrel object as the key
        barrel_entry = (need_priority, cur_barrel.price, cur_barrel)
        heapq.heappush(barrel_queue, barrel_entry)

    barrel_plan = []

    while barrel_queue:
        #print(barrel_queue)
        # Pop the barrel with the highest priority
        pop_result = heapq.heappop(barrel_queue)
        cur_barrel = pop_result[2]
        
        # Assuming cur_gold is the current budget
        max_quantity_affordable = cur_gold // cur_barrel.price
        quantity_to_buy = min(max_quantity_affordable, cur_barrel.quantity)

        print(cur_barrel.price)
        print(quantity_to_buy)

        total_price = (cur_barrel.price * quantity_to_buy)

        if total_price <= cur_gold:

            print(f"Buying {cur_barrel.potion_type} - {cur_barrel.sku}")
            print(f"Price: {total_price}")


            cur_gold -= total_price

            if cur_barrel.potion_type == [1, 0, 0, 0]:
                cur_red_ml += cur_barrel.ml_per_barrel * quantity_to_buy
            elif cur_barrel.potion_type == [0, 1, 0, 0]:
                cur_green_ml += cur_barrel.ml_per_barrel * quantity_to_buy
            elif cur_barrel.potion_type == [0, 0, 1, 0]:
                cur_blue_ml += cur_barrel.ml_per_barrel * quantity_to_buy
            elif cur_barrel.potion_type == [0, 0, 0, 1]:
                cur_dark_ml += cur_barrel.ml_per_barrel * quantity_to_buy

            barrel_plan.append(
                {
                    "sku": cur_barrel.sku,
                    "quantity": cur_barrel.quantity,
                }
            )

            # Re-calculate the need priority for the remaining barrels
            barrel_queue = [(priority, price, barrel) for priority, price, barrel in barrel_queue if barrel != cur_barrel]

    print(f" Gold: {cur_gold}")
    print(f" Red: {cur_red_ml}")
    print(f" Green: {cur_green_ml}")
    print(f" Blue: {cur_blue_ml}")
    print(f" Dark {cur_dark_ml}")

    print(barrel_plan)

    return barrel_plan




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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid potion type in barrels"
            )
        
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
'''