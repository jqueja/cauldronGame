import os
import dotenv
from sqlalchemy import create_engine

import sqlalchemy
from src import database as db

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

engine = create_engine(database_connection_url(), pool_pre_ping=True)



# RED POTIONS, CHANGE CHANGE CHAGNED
def get_red_potions():
    #print("In the helper GET red potions")

    query = """
    FROM global_inventory
    Select quantity
    WHERE sku = 'RED_POTION'
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_red_potions
    
def get_green_potions():
    #print("In the helper GET red potions")

    query = """
    FROM global_inventory
    Select quantity
    WHERE sku = 'GREEN_POTION'
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_green_potions
    
def get_blue_potions():
    #print("In the helper GET red potions")

    query = """
    FROM global_inventory
    Select quantity
    WHERE sku = 'BLUE_POTION'
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_blue_potions
    
def get_dark_potions():
    #print("In the helper GET red potions")

    query = """
    FROM global_inventory
    Select quantity
    WHERE sku = 'DARK_POTION'
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_dark_potions
    
def get_red_ml():
    #print("In the helper GET red mL")

    query = """SELECT num_red_ml FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_red_ml
    
def get_green_ml():
    #print("In the helper GET red mL")

    query = """SELECT num_green_ml FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_green_ml
    
def get_blue_ml():
    #print("In the helper GET red mL")

    query = """SELECT num_blue_ml FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_blue_ml
    
def get_blue_ml():
    #print("In the helper GET red mL")

    query = """SELECT num_blue_ml FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_blue_ml
    
def get_dark_ml():
    #print("In the helper GET red mL")

    query = """SELECT num_dark_ml FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_dark_ml
    
def get_gold():
    #print("In the helper GET gold")

    query = """SELECT gold FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.gold
    
'''
def set_red_potions(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_red_potions = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    
    
def set_red_ml(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_red_ml = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num

# GREEN POTIONS
def get_green_potions():
    #print("In the helper GET red potions")

    query = """SELECT num_green_potions FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_green_potions
    
def set_green_potions(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_green_potions = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    

    
def set_green_ml(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_green_ml = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num

# BLUE POTIONS
def get_blue_potions():
    #print("In the helper GET blue potions")

    query = """SELECT num_blue_potions FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_blue_potions
    
def set_blue_potions(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_blue_potions = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    
    
def set_blue_ml(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET num_blue_ml = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num
    
def get_dark_potions():
    #print("In the helper GET red potions")

    query = """SELECT num_dark_potions FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_dark_potions
    
def get_blue_ml():
    #print("In the helper GET red mL")

    query = """SELECT num_blue_ml FROM global_inventory"""

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_blue_ml
    



# GOLD STUFF
    
def set_gold(num):
    #print("In the helper SET red potions")

    query = f"""
    UPDATE global_inventory SET gold = {num}
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        
        return num


NOTE: Future implementations for helper functions.

    1) Have one function that takes in PARAMS: (Potions type and set)
        - set_potion(type of potion,) GET/SET

'''