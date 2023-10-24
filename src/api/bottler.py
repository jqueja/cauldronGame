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


            # Potion Transaction - id
            with db.engine.begin() as connection:
                description = f"Adding this potion {cur_potion.potion_type}"
                potion_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO potion_transactions (description)
                        VALUES (:description)
                        RETURNING id;
                        """
                    ),
                    {"description": description}
                )
                potions_transaction_id = potion_result.scalar()

            # Catalog id
            with db.engine.begin() as connection:
                cur_potion_result = connection.execute(
                    sqlalchemy.text(
                        """
                        SELECT id
                        FROM catalog
                        WHERE potion_type = :cur_potion_type;
                        """
                    ),
                    {"cur_potion_type": cur_potion.potion_type}
                )
                cur_potion_id = cur_potion_result.scalar()  

            # Ledger this into our db
            with db.engine.begin() as connection:
                catalog_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO potion_ledger_entries (potion_id, potion_transactions_id, inventory)
                        VALUES (:potion_id, :potion_transactions_id, 1)
                        """
                    ),
                    [{"potion_id": cur_potion_id, "potion_transactions_id": potions_transaction_id}])
                

            #  Update ml
            with db.engine.begin() as connection:
                description = f"Taking away for this potion: {cur_potion.potion_type}"
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

            # Red ml
            with db.engine.begin() as connection:
                red_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_ledger_entries (ml_transactions_id, red_ml)
                        VALUES (:ml_action_id, :red_ml)
                        """
                    ),
                    [{"ml_action_id": ml_action_id, "red_ml": red_index * -1}])
                
            # Green ml
            with db.engine.begin() as connection:
                green_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_ledger_entries (ml_transactions_id, green_ml)
                        VALUES (:ml_action_id, :green_ml)
                        """
                    ),
                    [{"ml_action_id": ml_action_id, "green_ml": green_index * -1}])
                
            # Blue ml
            with db.engine.begin() as connection:
                blue_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_ledger_entries (ml_transactions_id, blue_ml)
                        VALUES (:ml_action_id, :blue_ml)
                        """
                    ),
                    [{"ml_action_id": ml_action_id, "blue_ml": blue_index * -1}])
                
            # dark ml
            with db.engine.begin() as connection:
                dark_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_ledger_entries (ml_transactions_id, dark_ml)
                        VALUES (:ml_action_id, :dark_ml)
                        """
                    ),
                    [{"ml_action_id": ml_action_id, "dark_ml": dark_index * -1}])
                
            '''
            with db.engine.begin() as connection:
                connection.execute(
                    sqlalchemy.text(
                        """
                        UPDATE catalog SET
                        inventory = inventory + 1
                        WHERE potion_type = :potion_type
                        """),
                [{"potion_type": cur_potion.potion_type}])
            '''

  
    
    return "ok"
    

@router.post("/plan")
def get_bottle_plan():

        with db.engine.begin() as connection:
            empty_potions = connection.execute(
            sqlalchemy.text(
                """
                SELECT name, potion_type
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