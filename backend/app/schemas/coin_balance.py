from pydantic import BaseModel, ConfigDict


class CoinBalanceResponse(BaseModel):
    id: int
    balance: int

    model_config = ConfigDict(from_attributes=True)