from fastapi import status, HTTPException, Depends, APIRouter
from .schemas import UserCreate, UserResponse
from .database import engine, get_db
from . import models, utils
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
  prefix="/users",
  tags=['Users']
)

# function for creating users
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

  # create hash of password
  hash_pwd = utils.password_encoder(user.password)
  # update the pydantic model UserCreate
  user.password = hash_pwd

  new_user = models.User(**user.dict())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  return new_user

# get user by id
@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

  user = db.query(models.User).filter(models.User.id == id).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
  
  return user