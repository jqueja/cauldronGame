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

    setRedPotions(0)
    setRedml(0)
    setGold(100)

    return "OK"


@router.get("/shop_info/")
def get_shop_info():
    """ """

    # TODO: Change me!
    return {
        "shop_name": "StopNShop",
        "shop_owner": "Josh Queja",
    }

