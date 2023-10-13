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

    set_red_potions(0)
    set_green_potions(0)
    set_blue_potions(0)
    set_red_ml(0)
    set_green_ml(0)
    set_blue_ml(0)
    set_gold(100)


    # clears the global dct

    #global dctCart
    #dctCart.clear()

    #print(dctCart)


    return "OK"


@router.get("/shop_info/")
def get_shop_info():
    """ """

    # TODO: Change me!
    return {
        "shop_name": "StopNShop",
        "shop_owner": "Josh Queja",
    }

