from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .db import database
from .routers import transactions, users
# from .db.database import get_db
from sqlalchemy.orm import Session
from .core import oauth2, utils
from .schemas.user import Token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


# Connect models
models.Base.metadata.create_all(bind=database.engine)

# Init app object
app = FastAPI()


# resolving all cors object
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


# Login Route
# Login Path
@app.post("/login",
          response_model=Token
          )
def login(userCredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.username == userCredentials.username).first()

    # check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # check if password entered and the hashed are te same
    if not utils.verify(userCredentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    # create acess and refresh tokens
    access_token = oauth2.create_acess_token(
        data={"user_id": user.id})
    # user_dict = user.cop
    return {"access_token": access_token, "token_type": "bearer"}

    # URL to POST(Create) a user


# Include routers into the main app
app.include_router(transactions.router)
app.include_router(users.router)
