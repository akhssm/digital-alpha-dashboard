from datetime import datetime

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import (
    TransactionListResponse,
    TransactionResponse,
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


# ============================================================
# GET ALL TRANSACTIONS
# Supports:
# - pagination
# - category filtering
# - status filtering
# - merchant search
# - date range filtering
# - amount range filtering
# - sorting
# ============================================================

@router.get(
    "/",
    response_model=TransactionListResponse,
)
def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),

    category: str | None = Query(None),
    status: str | None = Query(None),
    search: str | None = Query(None),

    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),

    min_amount: float | None = Query(None, ge=0),
    max_amount: float | None = Query(None, ge=0),

    sort_by: str = Query("timestamp"),
    sort_order: str = Query("desc"),

    db: Session = Depends(get_db),
):
    # --------------------------------------------------------
    # Validate amount range
    # --------------------------------------------------------

    if (
        min_amount is not None
        and max_amount is not None
        and min_amount > max_amount
    ):
        raise HTTPException(
            status_code=400,
            detail="min_amount cannot be greater than max_amount",
        )

    # --------------------------------------------------------
    # Validate date range
    # --------------------------------------------------------

    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be after end_date",
        )

    # --------------------------------------------------------
    # Validate sorting
    # --------------------------------------------------------

    sort_columns = {
        "timestamp": Transaction.timestamp,
        "amount": Transaction.amount,
    }

    if sort_by not in sort_columns:
        raise HTTPException(
            status_code=400,
            detail="sort_by must be 'timestamp' or 'amount'",
        )

    if sort_order not in {"asc", "desc"}:
        raise HTTPException(
            status_code=400,
            detail="sort_order must be 'asc' or 'desc'",
        )

    # --------------------------------------------------------
    # Base query
    # --------------------------------------------------------

    query = select(Transaction)

    # --------------------------------------------------------
    # Category filter
    # --------------------------------------------------------

    if category:
        query = query.where(
            Transaction.category == category
        )

    # --------------------------------------------------------
    # Status filter
    # --------------------------------------------------------

    if status:
        query = query.where(
            Transaction.status == status
        )

    # --------------------------------------------------------
    # Merchant search
    # --------------------------------------------------------

    if search:
        query = query.where(
            Transaction.merchant.ilike(f"%{search}%")
        )

    # --------------------------------------------------------
    # Date range filter
    # --------------------------------------------------------

    if start_date is not None:
        query = query.where(
            Transaction.timestamp >= start_date
        )

    if end_date is not None:
        query = query.where(
            Transaction.timestamp <= end_date
        )

    # --------------------------------------------------------
    # Amount range filter
    # --------------------------------------------------------

    if min_amount is not None:
        query = query.where(
            Transaction.amount >= min_amount
        )

    if max_amount is not None:
        query = query.where(
            Transaction.amount <= max_amount
        )

    # --------------------------------------------------------
    # Count total matching transactions
    # --------------------------------------------------------

    count_query = select(
        func.count()
    ).select_from(
        query.subquery()
    )

    total = db.execute(count_query).scalar_one()

    # --------------------------------------------------------
    # Sorting
    # --------------------------------------------------------

    sort_column = sort_columns[sort_by]

    if sort_order == "desc":
        query = query.order_by(
            sort_column.desc()
        )
    else:
        query = query.order_by(
            sort_column.asc()
        )

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------

    query = (
        query
        .offset(skip)
        .limit(limit)
    )

    transactions = db.execute(
        query
    ).scalars().all()

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return TransactionListResponse(
        items=transactions,
        total=total,
        skip=skip,
        limit=limit,
    )


# ============================================================
# GET SINGLE TRANSACTION
# Used when the user clicks a transaction row
# ============================================================

@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
)
def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
):
    transaction = db.execute(
        select(Transaction).where(
            Transaction.id == transaction_id
        )
    ).scalar_one_or_none()

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    return transaction