from typing import Optional
from unittest.mock import Base
from pydantic import BaseModel
from datetime import datetime


# schema for Token


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    name: Optional[str]
    username: str
    created_at: datetime
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
    pass

    class Config:
        orm_mode = True
