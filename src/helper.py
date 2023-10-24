import os
import dotenv
from sqlalchemy import create_engine

import sqlalchemy
from src import database as db


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

        if cur_red_ml == None:
            return 0
        
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

        if cur_green_ml == None:
            return 0

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

        if cur_blue_ml == None:
            return 0

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

        if cur_dark_ml == None:
            return 0

        print(cur_dark_ml)
        return cur_dark_ml
     
def get_red_potions():
    with db.engine.begin() as connection:
        red_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM catalog
                WHERE name = 'red potion';
                """
            ),
        )
        red_id = red_result.scalar()
        print(f"This is the red id: {red_id}")

    with db.engine.begin() as connection:
        sum_red_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT SUM(inventory) AS amount
                FROM potion_ledger_entries
                WHERE potion_id = :red_id
                """ 
                ),
                {"red_id": red_id}
        )
        red_sum = sum_red_result.scalar()

        if red_sum is None:
            return 0

        print(red_sum)
        return red_sum
    
def get_green_potions():
    with db.engine.begin() as connection:
        green_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM catalog
                WHERE name = 'green potion';
                """
            ),
        )
        green_id = green_result.scalar()
        print(f"This is the green id: {green_id}")

    with db.engine.begin() as connection:
        sum_green_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT SUM(inventory) AS amount
                FROM potion_ledger_entries
                WHERE potion_id = :green_id
                """ 
                ),
                {"green_id": green_id}
        )
        green_sum = sum_green_result.scalar()

        if green_sum is None:
            return 0

        return green_sum
    
def get_blue_potions():
    with db.engine.begin() as connection:
        blue_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM catalog
                WHERE name = 'blue potion';
                """
            ),
        )
        blue_id = blue_result.scalar()

    with db.engine.begin() as connection:
        sum_blue_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT SUM(inventory) AS amount
                FROM potion_ledger_entries
                WHERE potion_id = :blue_id
                """
            ),
            {"blue_id": blue_id}
        )
        blue_sum = sum_blue_result.scalar()

        if blue_sum is None:
            return 0

        return blue_sum

def get_dark_potions():
    with db.engine.begin() as connection:
        dark_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT id
                FROM catalog
                WHERE name = 'dark potion';
                """
            ),
        )
        dark_id = dark_result.scalar()

    with db.engine.begin() as connection:
        sum_dark_result = connection.execute(
            sqlalchemy.text(
                """
                SELECT SUM(inventory) AS amount
                FROM potion_ledger_entries
                WHERE potion_id = :dark_id
                """
            ),
            {"dark_id": dark_id}
        )
        dark_sum = sum_dark_result.scalar()

        if dark_sum is None:
            return 0

        return dark_sum
