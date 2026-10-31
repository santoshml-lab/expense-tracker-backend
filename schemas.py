from datetime import date
from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
    description: str
    amount: float
    transaction_type: str
    category: str
    date: date


class TransactionResponse(TransactionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
