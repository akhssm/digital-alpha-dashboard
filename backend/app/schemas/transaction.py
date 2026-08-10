from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    timestamp: datetime
    merchant: str
    category: str | None
    amount: Decimal
    currency: str
    status: str
    payment_method: str


class TransactionListResponse(BaseModel):
    items: list[TransactionResponse]
    total: int
    skip: int
    limit: int