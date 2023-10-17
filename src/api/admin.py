from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

from ..database import *


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():
    """
    Reset the game state. Gold goes to 100, all potions are removed from
    inventory, and all barrels are removed from inventory. Carts are all reset.
    """

    with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                UPDATE global_inventory
                SET gold = 100, num_red_ml = 0, num_green_ml = 0,
                num_blue_ml = 0, num_dark_ml = 0
                """),
            )
    
    with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                UPDATE catalog
                SET inventory = 0
                """),
            )

    with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                DELETE
                FROM cart
                """),
            )
            

    return "OK"


@router.get("/shop_info/")
def get_shop_info():
    """ """

    # TODO: Change me!
    return {
        "shop_name": "StopNShop",
        "shop_owner": "Josh Queja",
    }

