from typing import Optional, List
from unittest.mock import Base
from pydantic import BaseModel
from datetime import datetime
from .transaction import TransactionResponse

# schema for Token


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    name: Optional[str]
    username: str
    created_at: Optional[datetime]
    balance: float

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserResponse(UserBase):
    id: Optional[int]
    income: float
    expenses: float
    transactions: list[TransactionResponse]

    class Config:
        orm_mode = True
