from passlib.context import CryptContext

# setting hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash the password
def hash(password: str):
    return pwd_context.hash(password)


# Verify if password entered and the hashed are te same
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

