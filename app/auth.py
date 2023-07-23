from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import database, schemas, models, utils, oauth2


router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  # OAuth2PasswordRequestForm return only 2 fields => username & password as Dict
    
  user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
  
  # verifying plain_text to hashed password from db
  if not utils.password_matcher(user_credentials.password, user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
  
  # create a token and return
  # we can pass in the data as we like
  access_token = oauth2.create_access_token(data={"user_id": user.id})

  return {"access_token": access_token, "token_type": "bearer"}