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

    print(barrels_delivered)

    gold_paid = 0
    red_ml = 0
    blue_ml = 0
    green_ml = 0
    dark_ml = 0

    for barrel_delivered in barrels_delivered:
        gold_paid += barrel_delivered.price * barrel_delivered.quantity
        print(f"This is gold paid: {gold_paid}")

        # Red Potion
        if barrel_delivered.potion_type == [1,0,0,0]:
            red_ml += barrel_delivered.ml_per_barrel * barrel_delivered.quantity

            # Red Ledger
            with db.engine.begin() as connection:
                description = f"Adding this red_ml {red_ml}"
                ml_result_red = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_transactions (description)
                        VALUES (:description)
                        RETURNING id;
                        """
                    ),
                    {"description": description}
                )
                ml_action_id = ml_result_red.scalar()

            with db.engine.begin() as connection:
                catalog_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_ledger_entries (ml_transactions_id, red_ml)
                        VALUES (:ml_action_id, :red_ml)
                        """
                    ),
                    [{"ml_action_id": ml_action_id, "red_ml": red_ml}])


        # Green Potion
        elif barrel_delivered.potion_type == [0, 1, 0, 0]:
            green_ml += barrel_delivered.ml_per_barrel * barrel_delivered.quantity

            print('IN GREEN')

            # Green Ledger
            with db.engine.begin() as connection:
                description = f"Adding this green_ml {green_ml}"
                ml_result_green  = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_transactions (description)
                        VALUES (:description)
                        RETURNING id;
                        """
                    ),
                    {"description": description}
                )
                ml_action_id = ml_result_green.scalar()

            with db.engine.begin() as connection:
                catalog_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_ledger_entries (ml_transactions_id, green_ml)
                        VALUES (:ml_action_id, :green_ml)
                        """
                    ),
                    [{"ml_action_id": ml_action_id, "green_ml": green_ml}])

        # Blue Potion
        elif barrel_delivered.potion_type == [0, 0, 1, 0]:
            blue_ml += barrel_delivered.ml_per_barrel * barrel_delivered.quantity

            # Blue Ledger
            with db.engine.begin() as connection:
                description = f"Adding this blue_ml {blue_ml}"
                ml_result_blue = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_transactions (description)
                        VALUES (:description)
                        RETURNING id;
                        """
                    ),
                    {"description": description}
                )
                ml_action_id = ml_result_blue.scalar()

            with db.engine.begin() as connection:
                catalog_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_ledger_entries (ml_transactions_id, blue_ml)
                        VALUES (:ml_action_id, :blue_ml)
                        """
                    ),
                    [{"ml_action_id": ml_action_id, "blue_ml": blue_ml}]
                )



        # Dark Potion
        elif barrel_delivered.potion_type == [0, 0, 0, 1]:
            dark_ml += barrel_delivered.ml_per_barrel * barrel_delivered.quantity

            # Dark Ledger
            with db.engine.begin() as connection:
                description = f"Adding this dark_ml {dark_ml}"
                ml_result_dark = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_transactions (description)
                        VALUES (:description)
                        RETURNING id;
                        """
                    ),
                    {"description": description}
                )
                ml_action_id = ml_result_dark.scalar()

            with db.engine.begin() as connection:
                catalog_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_ledger_entries (ml_transactions_id, dark_ml)
                        VALUES (:ml_action_id, :dark_ml)
                        """
                    ),
                    [{"ml_action_id": ml_action_id, "dark_ml": dark_ml}]
                )


        else:
            raise Exception("Invalid potion type")
        
        print(gold_paid)
        with db.engine.begin() as connection:
                description = f"Buying this barrel: {barrel_delivered.sku} with cost of {gold_paid}"
                catalog_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO gold_transactions (description)
                        VALUES (:description)
                        RETURNING id;
                        """
                    ),
                    {"description": description}
                )
                gold_action_id = catalog_result.scalar()

        minus_value = gold_paid * -1
        
        with db.engine.begin() as connection:
                catalog_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO gold_ledger_entries (gold_transactions_id, change)
                        VALUES (:gold_action_id, :change)
                        """
                    ),
                    {"gold_action_id": gold_action_id, "change":minus_value}
            )
        
    print(f"gold_paid: {gold_paid}, red_ml: {red_ml}, blue_ml: {blue_ml}, dark_ml: {dark_ml}")

    '''
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
    '''
    
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
            print(cur_barrel.sku)
            purchase_plan.append(
                {
                    "sku": cur_barrel.sku,
                    "quantity": 1,
                }
            )

        elif (cur_blue_ml <= 100) and (cur_barrel.price <= cur_gold) and (cur_barrel.potion_type == [0, 0, 1, 0]):
            cur_blue_ml += cur_barrel.ml_per_barrel
            cur_gold -= (cur_barrel.price * 1)
            print(cur_barrel.sku)
            purchase_plan.append(
                {
                    "sku": cur_barrel.sku,
                    "quantity": 1,
                }
            )

        elif (cur_dark_ml <= 50) and (cur_barrel.price <= cur_gold) and (cur_barrel.potion_type == [0, 0, 0, 1]):
            cur_dark_ml += cur_barrel.ml_per_barrel
            cur_gold -= (cur_barrel.price * 1)
            print(cur_barrel.sku)
            purchase_plan.append(
                {
                    "sku": cur_barrel.sku,
                    "quantity": 1,
                }
            )
    print(purchase_plan)
    return purchase_plan
