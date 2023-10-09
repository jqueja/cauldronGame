import os
import dotenv
from sqlalchemy import create_engine

import sqlalchemy
from src import database as db

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

engine = create_engine(database_connection_url(), pool_pre_ping=True)



# RED POTIONS
def getRedPotions():
    #print("In the helper GET red potions")

    query = """SELECT num_red_potions FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_red_potions
    
def setRedPotions(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_red_potions = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    
def getRedml():
    #print("In the helper GET red mL")

    query = """SELECT num_red_ml FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_red_ml
    
def setRedml(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_red_ml = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    



# GREEN POTIONS
def getGreenPotions():
    #print("In the helper GET red potions")

    query = """SELECT num_green_potions FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_green_potions
    
def setGreenPotions(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_green_potions = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    
def getGreenml():
    #print("In the helper GET red mL")

    query = """SELECT num_green_ml FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_green_ml
    
def setGreenml(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_green_ml = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    






# BLUE POTIONS
def getBluePotions():
    #print("In the helper GET blue potions")

    query = """SELECT num_blue_potions FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_blue_potions
    
def setBluePotions(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_blue_potions = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    

def getBlueml():
    #print("In the helper GET red mL")

    query = """SELECT num_blue_ml FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_blue_ml
    
def setBlueml(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_blue_ml = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num






    

        

    

# GOLD STUFF
def getGold():
    #print("In the helper GET gold")

    query = """SELECT gold FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.gold
    
def setGold(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET gold = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num


'''
NOTE: Future implementations for helper functions.

    1) Have one function that takes in PARAMS: (Potions type and set)
        - setPotion(type of potion,) GET/SET
'''