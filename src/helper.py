import os
import dotenv
from sqlalchemy import create_engine

import sqlalchemy
from src import database as db


def red_potion_change(num):
   
   with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE catalog
                SET 
                quantity = quantity + :num
                WHERE sku = 'RED_POTION'
                """),
        [{"num": num, }])

def red_ml_change(num):
   
   with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE global_inventory
                SET
                num_red_ml = num_red_ml + :num
                """),
        [{"num": num, }])




def green_potion_change(num):
   
   with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE catalog
                SET 
                quantity = quantity + :num
                WHERE sku = 'GREEN_POTION'
                """),
        [{"num": num, }])

def green_ml_change(num):
   
   with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE global_inventory
                SET
                num_green_ml = num_green_ml + :num
                """),
        [{"num": num, }])


def blue_potion_change(num):
   
   with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE catalog
                SET 
                quantity = quantity + :num
                WHERE sku = 'BLUE_POTION'
                """),
        [{"num": num, }])

def blue_ml_change(num):
   
   with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE global_inventory
                SET
                num_blue_ml = num_blue_ml + :num
                """),
        [{"num": num, }])

def dark_potion_change(num):
   
   with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE catalog
                SET 
                quantity = quantity + :num
                WHERE sku = 'DARK_POTION'
                """),
        [{"num": num, }])

def dark_ml_change(num):
   
   with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                UPDATE global_inventory
                SET
                num_dark_ml = num_dark_ml + :num
                """),
        [{"num": num, }])        

    # what do I return (how can I add some error checking in my code)


def get_gold():
    with db.engine.begin() as connection:
        gold_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT SUM(change) AS balance
                FROM gold_ledger_entries
                """),
        )
        cur_gold = gold_result.scalar()

        print(cur_gold)
        return cur_gold
