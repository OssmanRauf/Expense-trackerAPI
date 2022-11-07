from decimal import Decimal
from ..core import oauth2
from .. import models
from ..db.database import get_db
from sqlalchemy.orm import Session, contains_eager, joinedload
from fastapi import Depends, status, HTTPException, Response, APIRouter
from ..schemas.transaction import TransactionResponse, TransactionCreate


# Init router object
router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

# URL to POST(Create) a post


@ router.post("/", response_model=TransactionResponse,  status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    print(current_user)
    user = db.query(models.User).filter(
        models.User.id == current_user.id)
    value = Decimal(transaction.transaction_value)
    print(value)
    if transaction.is_income:
        user.update({"balance": user.first().balance +
                    value, "income": user.first().income+value},  synchronize_session=False)
    else:
        user.update({"balance": user.first().balance -
                     value, "expenses": user.first().expenses+value}, synchronize_session=False)
    new_transaction = models.Transaction(
        account_id=current_user.id, **transaction.dict())

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


# GET post by ID
@ router.get("/", status_code=status.HTTP_200_OK, response_model=list[TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.account_id == current_user.id).all()

    return transaction


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(
        models.User.id == current_user.id)
    user = user_query.first()
    transaction_query = db.query(models.Transaction).filter(
        models.Transaction.id == id)
    transaction = transaction_query.first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if transaction.account_id == current_user.id:
        if transaction.is_income:
            user_query.update({"balance": user.balance -
                               transaction.transaction_value, "income": user.income-transaction.transaction_value})
        else:
            user_query.update({"balance": user.balance +
                               transaction.transaction_value, "expenses": user.expenses-transaction.transaction_value})
        transaction_query.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
