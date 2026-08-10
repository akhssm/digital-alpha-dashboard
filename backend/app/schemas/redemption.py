from pydantic import BaseModel


class RedemptionResponse(BaseModel):
    message: str
    reward_id: int
    reward_name: str
    coins_spent: int
    remaining_balance: int