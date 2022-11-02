from decimal import Decimal
from ..core import oauth2, utils
from .. import models
from ..schemas.user import Token, UserCreate, UserResponse
from ..db.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# Init router object
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    username = db.query(models.User).filter(
        models.User.username == user.username).first()

    # check if username is taken
    if username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Username taken pleasse try again")

    # hash password with utils function
    user.password = utils.hash(user.password)
    user.balance = Decimal(user.balance)
    # user.username = user.username.lower()
    # create user

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/all", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    return user
