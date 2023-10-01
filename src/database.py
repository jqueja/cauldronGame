import os
import dotenv
from sqlalchemy import create_engine

import sqlalchemy
from src import database as db

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

engine = create_engine(database_connection_url(), pool_pre_ping=True)

def getRedPotions():
    #print("In the helper GET red potions")

    query = "SELECT num_red_potions FROM global_inventory"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_red_potions
    
def getRedml():
    #print("In the helper GET red mL")

    query = "SELECT num_red_ml FROM global_inventory"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_red_ml
    
def getGold():
    #print("In the helper GET gold")

    query = "SELECT gold FROM global_inventory"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.gold
    
def setRedPotions(num):
    #print("In the helper SET red potions")

    query = f"UPDATE global_inventory SET num_red_potions = {num}"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    
def setRedml(num):
    #print("In the helper SET red potions")

    query = f"UPDATE global_inventory SET num_red_ml = {num}"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    
def setGold(num):
    #print("In the helper SET red potions")

    query = f"UPDATE global_inventory SET gold = {num}"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    