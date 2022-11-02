from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .. import models
from fastapi.security import OAuth2PasswordBearer
from ..db.database import get_db
from sqlalchemy.orm import Session
from .config import settings
from ..schemas import user

#
# asks for credentials
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# extracting envirement variebles from settings class
SECREAT_KEY = settings.secreat_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRATION_DAYS = settings.access_token_expiration_days
# REFRESH_TOKEN_EXPIRATION_TIME = settings.refresh_token_expiration_time


# functian that create a acess token that aspects a user dict as parameter
def create_acess_token(data: dict):
    # copy the dict so that we can encode
    to_encode = data.copy()
    # create expire date of the token
    expire = datetime.utcnow() + timedelta(minutes=0, hours=0,
                                           days=ACCESS_TOKEN_EXPIRATION_DAYS)
    # update the dict that will be encoded
    to_encode.update({"exp": expire,
                      "scope": "access token"})

    print("Updated")

    # creating the token
    access_token = jwt.encode(to_encode, SECREAT_KEY, algorithm=ALGORITHM)

    return access_token


# function to verify the access token takes as parameter the token and the exception
def verify_access_token(access_token: str, credentials_exceptions):

    # try:
    # creating the payload decoding the token
    payload = jwt.decode(access_token, SECREAT_KEY, algorithms=[ALGORITHM])

    # get the id from the payload
    id: str = payload.get("user_id")

    # if exp < datetime.utcnow():
    #     refresh_token()

    # Check if id exists in the payload and if the token is not a refresh token
    if id is None or payload.get("scope") == "refresh token":
        raise credentials_exceptions

    # puts the id in the varieble token_data
    token_data = dict({"user_id": id})

    return token_data


# get current user from acess token (the function thatwill be called in all the routes)
def get_current_user(access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # create an exception
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    # using the verify_access_token function and passing the acess token and the exception
    data = verify_access_token(access_token, credentials_exceptions)
    print(data["user_id"])
    user = db.query(models.User).filter(
        models.User.id == data["user_id"]).first()

    return user
