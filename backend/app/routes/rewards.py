from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.reward import Reward
from app.models.coin_balance import CoinBalance
from app.schemas.reward import RewardResponse
from app.schemas.redemption import RedemptionResponse


router = APIRouter(
    prefix="/rewards",
    tags=["Rewards"],
)


# --------------------------------------------------
# GET REWARDS
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[RewardResponse],
)
def get_rewards(
    db: Session = Depends(get_db),
):
    rewards = db.execute(
        select(Reward)
        .where(Reward.is_active.is_(True))
        .order_by(Reward.coin_cost.asc())
    ).scalars().all()

    return rewards


# --------------------------------------------------
# REDEEM REWARD
# --------------------------------------------------

@router.post(
    "/{reward_id}/redeem",
    response_model=RedemptionResponse,
)
def redeem_reward(
    reward_id: int,
    db: Session = Depends(get_db),
):
    # 1. Check whether reward exists
    reward = db.execute(
        select(Reward)
        .where(Reward.id == reward_id)
    ).scalar_one_or_none()

    if reward is None:
        raise HTTPException(
            status_code=404,
            detail="Reward not found",
        )

    # 2. Check whether reward is active
    if not reward.is_active:
        raise HTTPException(
            status_code=400,
            detail="Reward is not active",
        )

    # 3. Get coin balance and lock the row
    coin_balance = db.execute(
        select(CoinBalance)
        .where(CoinBalance.id == 1)
        .with_for_update()
    ).scalar_one_or_none()

    if coin_balance is None:
        raise HTTPException(
            status_code=404,
            detail="Coin balance not found",
        )

    # 4. Check sufficient balance
    if coin_balance.balance < reward.coin_cost:
        raise HTTPException(
            status_code=400,
            detail="Insufficient coin balance",
        )

    # 5. Deduct coins
    coin_balance.balance -= reward.coin_cost

    # 6. Commit safely
    try:
        db.commit()
        db.refresh(coin_balance)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to redeem reward",
        )

    # 7. Return successful response
    return RedemptionResponse(
        message="Reward redeemed successfully",
        reward_id=reward.id,
        reward_name=reward.name,
        coins_spent=reward.coin_cost,
        remaining_balance=coin_balance.balance,
    )