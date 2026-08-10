from pydantic import BaseModel, ConfigDict


class RewardResponse(BaseModel):
    id: int
    name: str
    description: str
    coin_cost: int
    reward_type: str
    value: float
    is_active: bool

    model_config = ConfigDict(from_attributes=True)