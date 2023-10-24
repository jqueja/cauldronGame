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
    
def get_red_ml():
     with db.engine.begin() as connection:
        red_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT SUM(red_ml) AS amount
                FROM ml_ledger_entries
                """),
        )
        cur_red_ml = red_result.scalar()

        print(cur_red_ml)
        return cur_red_ml
     
def get_green_ml():
     with db.engine.begin() as connection:
        green_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT SUM(green_ml) AS amount
                FROM ml_ledger_entries
                """),
        )
        cur_green_ml = green_result.scalar()

        print(cur_green_ml)
        return cur_green_ml

def get_blue_ml():
     with db.engine.begin() as connection:
        blue_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT SUM(blue_ml) AS amount
                FROM ml_ledger_entries
                """),
        )
        cur_blue_ml = blue_result.scalar()

        print(cur_blue_ml)
        return cur_blue_ml

def get_dark_ml():
     with db.engine.begin() as connection:
        dark_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT SUM(dark_ml) AS amount
                FROM ml_ledger_entries
                """),
        )
        cur_dark_ml = dark_result.scalar()

        print(cur_dark_ml)
        return cur_dark_ml
