from datetime import datetime

from sqlalchemy import DateTime, Numeric, String, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    merchant: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    amount: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True
    )

    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


Index(
    "ix_transactions_timestamp_category",
    Transaction.timestamp,
    Transaction.category
)