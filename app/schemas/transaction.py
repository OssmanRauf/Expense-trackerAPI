from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base user Schema


class TransactionBase(BaseModel):
    transaction_date: Optional[datetime]
    is_income: bool
    # transaction_type: Optional[str]
    description: Optional[str]
    transaction_value: float

    class Config:
        orm_mode = True


class TransactionCreate(TransactionBase):

    class Config:
        orm_mode = True


class TransactionResponse(TransactionBase):
    id: Optional[int]
    account_id: int
