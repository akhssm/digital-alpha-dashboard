from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class CoinBalance(Base):
    __tablename__ = "coin_balance"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        default=1,
    )

    balance: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )