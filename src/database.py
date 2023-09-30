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
    print("In the helper get red potions")

    query = "SELECT num_red_potions FROM global_inventory"

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text(query))
        row = result.first()

        return row.num_red_potions
    
