from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import math

from ..database import *

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/inventory")
def get_inventory():

    total_potions = get_red_potions() + get_green_potions() + get_blue_potions() + get_dark_potions()
    total_ml = get_red_ml() + get_blue_ml() + get_green_ml() + get_dark_ml()

    return {"number_of_potions": total_potions,
        "ml_in_barrels": total_ml,
        "gold": get_gold()
        }


class Result(BaseModel):
    gold_match: bool
    barrels_match: bool
    potions_match: bool

# Gets called once a day
@router.post("/results")
def post_audit_results(audit_explanation: Result):
    """ """
    print(audit_explanation)

    return{
    "gold_match": audit_explanation.gold_match,
    "barrels_match": audit_explanation.barrels_match,
    "potions_match": audit_explanation.potions_match,
    }