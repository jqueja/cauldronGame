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

    return {"number_of_potions": getRedPotions(),
            "ml_in_barrels": getRedml(),
            "gold": getGold()
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

    return "OK"
