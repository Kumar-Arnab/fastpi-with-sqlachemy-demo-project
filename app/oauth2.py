from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# tokenUrl is the login endpoint of our app without the '/'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Required fields for token :=
# SECRET_KEY, Algorithm=HS256, Expiration_time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93E7099f6f0f4caa6cf63b88e8d4e0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # in minutes

# creating the JWT token
def create_access_token(data: dict):
  # keeping a copy of the original data
  to_encode =  data.copy()

  # setting the expiry time for token as (current_time + 30 minutes)
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

  # setting the expiry time to the data
  to_encode.update({"exp": expire})

  # generating the JWT token by passing the data, secret key and specifying the algorithm
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt


# function to verify access token
# decoding the token, extracting the id and storing it to a pydantic model and returning the value 
# returning exception if not found
def verify_access_token(token: str, credentials_exception):

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms={ALGORITHM})

    # now extract payload from the fields saved to token in auth.py while generating the access_token
    id: str = payload.get("user_id")

    if id is None:
      raise credentials_exception
    
    token_data = schemas.TokenData(id= id)
  except JWTError:
    raise credentials_exception
  
  return token_data
  

# it fetches the user from the db and verify if the token is correct
# this is the function which will be used to check protected endpoint access for user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"Could not validate credentials", 
    headers={"WWW-Authenticate": "Bearer"}
  )

  token = verify_access_token(token, credentials_exception)

  user = db.query(models.User).filter(models.User.id == token.id).first()
  return user