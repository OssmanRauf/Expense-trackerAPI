from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey


# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("NOW()"))
    balance = Column(Numeric(10, 2), nullable=False, default=0)
    income = Column(Numeric(10, 2), nullable=False, default=0)
    expenses = Column(Numeric(10, 2), nullable=False, default=0)


# Post Model(Table)
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, nullable=False)

    transaction_date = Column(TIMESTAMP(timezone=True),
                              nullable=False, server_default=text("NOW()"))
    is_income = Column(Boolean, nullable=False, server_default="False")
    transaction_type = Column(String, nullable=True)
    description = Column(String, nullable=True)
    account_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    transaction_value = Column(Numeric(10, 2), nullable=False)
