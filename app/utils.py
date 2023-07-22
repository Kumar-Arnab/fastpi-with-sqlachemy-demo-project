# It contains few utility functions
from passlib.context import CryptContext

# setting for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def password_encoder(password: str):
    return pwd_context.hash(password)