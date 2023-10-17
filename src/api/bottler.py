from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

from ..database import *
from ..helper import *



router = APIRouter(
    prefix="/bottler",
    tags=["bottler"],
    dependencies=[Depends(auth.get_api_key)],
)

class PotionInventory(BaseModel):
    potion_type: list[int]
    quantity: int

# Subtract the red mL I have, add red potions

# [0, 0, 0, 0]

# Instead of checking whether or not I can make it into a potion right away.
# What I can do is iterate through the diff indexes and add them together

# Is there a more efficient way to bottle

@router.post("/deliver")
def post_deliver_bottles(potions_delivered: list[PotionInventory]):

    cur_red_ml = get_red_ml()
    cur_green_ml = get_green_ml()
    cur_blue_ml = get_blue_ml()
    cur_dark_ml = get_dark_ml()

    for cur_potion in potions_delivered:
        red_index = cur_potion.potion_type[0]
        green_index = cur_potion.potion_type[1]
        blue_index = cur_potion.potion_type[2]
        dark_index = cur_potion.potion_type[3]

        '''
        red_max_quantity = cur_red_ml // red_index if red_index != 0 else float(1000)
        green_max_quantity = cur_green_ml // green_index if green_index != 0 else float(1000)
        blue_max_quantity = cur_blue_ml // blue_index if blue_index != 0 else float(1000)
        dark_max_quantity = cur_dark_ml // dark_index if dark_index != 0 else float(1000)

        print(red_index)
        print(red_max_quantity)
        print(green_index)
        print(green_max_quantity)
        print(blue_index)
        print(blue_max_quantity)
        print(dark_index)
        print(dark_max_quantity)
        min_max_quantity = min(red_max_quantity, green_max_quantity, blue_max_quantity, dark_max_quantity)
        '''

        # for now just do one, red_max_quantity
        if (
            cur_red_ml - red_index * 1 <= -1 or
            cur_green_ml - green_index * 1 <= -1 or
            cur_blue_ml - blue_index * 1 <= -1 or
            cur_dark_ml - dark_index * 1 <= -1
        ):  
            print(f"Not enough ingredients to make {cur_potion.potion_type}. Skipping...")
            continue
        
        print(f"enough ingredients to make {cur_potion.potion_type}. MONEY")
        with db.engine.begin() as connection:
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE catalog
                    SET inventory = inventory + 1 WHERE potion_type = :potion_type
                    """),
                [{"potion_type": cur_potion.potion_type}])

            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE global_inventory
                    SET num_red_ml = num_red_ml - :red_index * 1,
                        num_green_ml = num_green_ml - :green_index * 1,
                        num_blue_ml = num_blue_ml - :blue_index * 1,
                        num_dark_ml = num_dark_ml - :dark_index * 1
                    """),
                [{"red_index": red_index, "green_index": green_index, "blue_index": blue_index, "dark_index": dark_index}])

    return "ok"





@router.post("/plan")
def get_bottle_plan():
    bottle_plan = []
    cur_red_ml = get_red_ml()
    cur_green_ml = get_green_ml()
    cur_blue_ml = get_blue_ml()
    cur_dark_ml = get_dark_ml()

    print()

    while True:
        can_make_potion = False  # Flag to check if any potions can be made in this iteration

        with db.engine.begin() as connection:
            empty_potions = connection.execute(
            sqlalchemy.text(
                """
                SELECT name, potion_type, inventory
                FROM catalog
                ORDER BY catalog.priority ASC
                """
            )
        )

            potion_lst = empty_potions.fetchall()
            print(potion_lst)
            

            for potion in potion_lst:
                red_index, green_index, blue_index, dark_index = potion.potion_type
                print("--------")
                print(red_index)
                print(green_index)
                print(blue_index)
                print(dark_index)

                print("Current Red ML:", cur_red_ml)
                print("Current Green ML:", cur_green_ml)
                print("Current Blue ML:", cur_blue_ml)
                print("Current Dark ML:", cur_dark_ml)

                if (
                    red_index <= cur_red_ml
                    and green_index <= cur_green_ml
                    and blue_index <= cur_blue_ml
                    and dark_index <= cur_dark_ml
                ):
                    cur_red_ml -= red_index
                    cur_green_ml -= green_index
                    cur_blue_ml -= blue_index
                    cur_dark_ml -= dark_index

                    # Check if the potion type is already in the plan
                    potion_type_exists = False
                    for entry in bottle_plan:
                        if entry["potion_type"] == potion.potion_type:
                            entry["quantity"] += 1
                            potion_type_exists = True
                            break

                    # If the potion type is not in the plan, add a new entry
                    if not potion_type_exists:
                        bottle_plan.append(
                            {
                                "potion_type": potion.potion_type,
                                "quantity": 1,
                            }
                        )

                    can_make_potion = True  # Set the flag to True since a potion was made

        if not can_make_potion:
            break  # Exit the while loop if no more potions can be made

    print(bottle_plan)
    return bottle_plan




'''
@router.post("/plan")
def get_bottle_plan():

    with db.engine.begin() as connection:
        empty_potions = connection.execute(
        sqlalchemy.text(
            """
            SELECT name, potion_type, inventory
            FROM catalog
            WHERE inventory = 0
            """)
        )

        bottle_plan = []

        potion_lst = empty_potions.fetchall()

        print(f"bottler {potion_lst}")

        cur_red_ml = get_red_ml()
        cur_green_ml = get_green_ml()
        cur_blue_ml = get_blue_ml()
        cur_dark_ml = get_dark_ml()

        for cur_potion in potion_lst:
            print(cur_potion)
            red_index = cur_potion.potion_type[0]
            green_index = cur_potion.potion_type[1]
            blue_index = cur_potion.potion_type[2]
            dark_index = cur_potion.potion_type[3]

            if (red_index <= cur_red_ml) and (green_index <= cur_green_ml) and \
            (blue_index <= cur_blue_ml) and (dark_index <= cur_dark_ml):
                cur_red_ml  -= red_index
                cur_green_ml -= green_index
                cur_blue_ml -= blue_index
                cur_dark_ml -= dark_index

                bottle_plan.append(
                    {
                    "potion_type": cur_potion.potion_type,
                    "quantity": 1,
                    }
                )

    print(bottle_plan)

    connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE global_inventory
                    SET num_red_ml = num_red_ml - :red_index * :red_max_quantity,
                        num_green_ml = num_green_ml - :green_index * :green_max_quantity,
                        num_blue_ml = num_blue_ml - :blue_index * :blue_max_quantity,
                        num_dark_ml = num_dark_ml - :dark_index * :dark_max_quantity
                    """),
                [{"red_index": red_index, "green_index": green_index, "blue_index": blue_index, "dark_index": dark_index, "quantity": cur_potion.quantity, "red_max_quantity": red_max_quantity,
                  "green_max_quantity": green_max_quantity, "blue_max_quantity": blue_index, "dark_max_quantity": dark_max_quantity}])

    return bottle_plan
    '''