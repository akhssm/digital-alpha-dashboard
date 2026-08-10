from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.transaction import Transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/")
def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    transactions = db.execute(
        select(Transaction)
        .order_by(Transaction.timestamp.desc())
        .offset(skip)
        .limit(limit)
    ).scalars().all()

    return transactions