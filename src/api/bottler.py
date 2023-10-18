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

        # Potion recipe    
        red_index = cur_potion.potion_type[0]
        green_index = cur_potion.potion_type[1]
        blue_index = cur_potion.potion_type[2]
        dark_index = cur_potion.potion_type[3]

        # I can make the potioin
        if (cur_red_ml - red_index >= 0) and (cur_green_ml - green_index >= 0)\
        and (cur_blue_ml - blue_index >= 0) and (cur_dark_ml - dark_index >= 0):
            
            cur_red_ml -= red_index
            cur_green_ml -= green_index
            cur_blue_ml -= blue_index
            cur_dark_ml -= dark_index

            with db.engine.begin() as connection:
                connection.execute(
                    sqlalchemy.text(
                        """
                        UPDATE catalog SET
                        inventory = inventory + 1
                        WHERE potion_type = :potion_type
                        """),
                [{"potion_type": cur_potion.potion_type}])

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE global_inventory SET
                num_red_ml = :red_ml,
                num_green_ml = :green_ml,
                num_blue_ml = :blue_ml,
                num_dark_ml = :dark_ml
                """),
        [{"red_ml": cur_red_ml, "green_ml": cur_green_ml, "blue_ml": cur_blue_ml, "dark_ml": cur_dark_ml}])
    
    return "ok"
    

@router.post("/plan")
def get_bottle_plan():

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

        cur_red_ml = get_red_ml()
        cur_green_ml = get_green_ml()
        cur_blue_ml = get_blue_ml()
        cur_dark_ml = get_dark_ml()

        print(cur_red_ml)

        bottle_plan = []
        
        for cur_potion in potion_lst:
                
            red_index = cur_potion.potion_type[0]
            green_index = cur_potion.potion_type[1]
            blue_index = cur_potion.potion_type[2]
            dark_index = cur_potion.potion_type[3]

            if (cur_red_ml - red_index >= 0) and (cur_green_ml - green_index >= 0)\
            and (cur_blue_ml - blue_index >= 0) and (cur_dark_ml - dark_index >= 0):
                bottle_plan.append(
                            {
                                "potion_type": cur_potion.potion_type,
                                "quantity": 1,
                            }
                        )
                cur_red_ml -= red_index
                cur_green_ml -= green_index
                cur_blue_ml -= blue_index
                cur_dark_ml -= dark_index
        
        print(bottle_plan)
        return bottle_plan