from pydantic import BaseModel
from typing import Optional

class LoyaltyAccount(BaseModel):
    account_id: str
    program_name: str
    current_balance: int
    last_updated: Optional[str] = None
    metadata: Optional[dict] = None

    class Config:
        orm_mode = True

class Recommendation(BaseModel):
    id: str
    title: str
    description: str
    program_name: str
    points_required: int
    estimated_value: int
    confidence_score: float

    class Config:
        orm_mode = True
