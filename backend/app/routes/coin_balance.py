from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.coin_balance import CoinBalance
from app.schemas.coin_balance import CoinBalanceResponse


router = APIRouter(
    prefix="/coin-balance",
    tags=["Coin Balance"],
)


@router.get(
    "/",
    response_model=CoinBalanceResponse,
)
def get_coin_balance(
    db: Session = Depends(get_db),
):
    coin_balance = db.execute(
        select(CoinBalance)
        .where(CoinBalance.id == 1)
    ).scalar_one_or_none()

    if coin_balance is None:
        raise HTTPException(
            status_code=404,
            detail="Coin balance not found",
        )

    return coin_balance