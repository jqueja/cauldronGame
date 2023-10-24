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
    Reset the game state.
     Carts are all reset.
    """

    # Gold goes to 100 and all barrels are removed from inventory.
    with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                UPDATE global_inventory
                SET gold = 100, num_red_ml = 0, num_green_ml = 0,
                num_blue_ml = 0, num_dark_ml = 0
                """),
            )
    
    # inventory = 0,
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
                FROM cart_items
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

    # For Gold
    with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                DELETE
                FROM gold_ledger_entries
                """),
            )
    with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                DELETE
                FROM gold_transactions
                """),
            )

    # For ml
    with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                DELETE
                FROM ml_ledger_entries
                """),
            )
    with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                DELETE
                FROM ml_transactions
                """),
            )

    # For potions
    with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                DELETE
                FROM potion_ledger_entries
                """),
            )
    with db.engine.begin() as connection:
            connection.execute(
            sqlalchemy.text(
                """
                DELETE
                FROM potion_transactions
                """),
            )



    
    # This is for Gold
    with db.engine.begin() as connection:
                description = f"This is the start"
                catalog_result = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO gold_transactions (description)
                        VALUES (:description)
                        RETURNING id;
                        """
                    ),
                    {"description": description}
                )
                gold_action_id = catalog_result.scalar()

    with db.engine.begin() as connection:
            catalog_result = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO gold_ledger_entries (gold_transactions_id, change)
                    VALUES (:gold_action_id, 100)
                    """
                ),
                {"gold_action_id": gold_action_id}
            )

    '''
    # This is for red_ml
    with db.engine.begin() as connection:
                description = f"This is the start red_ml"
                ml_result_red = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_transactions (description)
                        VALUES (:description)
                        RETURNING id;
                        """
                    ),
                    {"description": description}
                )
                ml_action_id = ml_result_red.scalar()


    with db.engine.begin() as connection:
            catalog_result = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO ml_ledger_entries (ml_transactions_id, red_ml)
                    VALUES (:ml_action_id, 0)
                    """
                ),
                [{"ml_action_id": ml_action_id}])

            
    # This is for green_ml
    with db.engine.begin() as connection:
                description = f"This is the start green_ml"
                ml_result_green = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_transactions (description)
                        VALUES (:description)
                        RETURNING id;
                        """
                    ),
                    {"description": description}
                )
                ml_action_id = ml_result_green.scalar()


    with db.engine.begin() as connection:
            catalog_result = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO ml_ledger_entries (ml_transactions_id, green_ml)
                    VALUES (:ml_action_id, 0)
                    """
                ),
                [{"ml_action_id": ml_action_id}])
            
    # This is for blue_ml
    with db.engine.begin() as connection:
                description = f"This is the start blue_ml"
                ml_result_blue = connection.execute(
                    sqlalchemy.text(
                        """
                        INSERT INTO ml_transactions (description)
                        VALUES (:description)
                        RETURNING id;
                        """
                    ),
                    {"description": description}
                )
                ml_action_id = ml_result_blue.scalar()


    with db.engine.begin() as connection:
            catalog_result = connection.execute(
                sqlalchemy.text(
                    """
                    INSERT INTO ml_ledger_entries (ml_transactions_id, blue_ml)
                    VALUES (:ml_action_id, 0)
                    """
                ),
                [{"ml_action_id": ml_action_id}])
    '''

    return "OK"


@router.get("/shop_info/")
def get_shop_info():
    """ """

    # TODO: Change me!
    return {
        "shop_name": "StopNShop",
        "shop_owner": "Josh Queja",
    }

