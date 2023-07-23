from fastapi import Response, status, HTTPException, Depends, APIRouter
from .schemas import PostCreate, Post
from .database import engine, get_db
from . import models, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
  prefix="/posts",
  tags=['Posts']
)
# by mentioning the '/posts' we can remove the posts from every single api router.get with a simple '/'

# API to fetch all posts
# filtering by query params
@router.get("/", response_model=List[Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,
              skip: int = 0, search: Optional[str] = ""):

  # if no limit is provided it takes the default limit of 10
  # offset will skip the no of mentioned records from the top of db schema like skip = 3 skips first 3 records
  posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  print(f"logged in user {current_user.email} with query param limit: {limit}")

  return posts

# title string, content string for post payload
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

  print(f"logged in user_id {current_user.id}")
  new_post = models.Post(user_id=current_user.id, **post.dict())
  db.add(new_post)
  db.commit()
  # retrieve the new_post and store it in new_post variable
  db.refresh(new_post)

  return new_post

@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  post = db.query(models.Post).filter(models.Post.id == id).first()

  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
  if post.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform requested action")

  return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  post_query = db.query(models.Post).filter(models.Post.id == id)

  if post_query.first() is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
  if post_query.first().user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform requested action")
  
  post_query.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  post_query = db.query(models.Post).filter(models.Post.id == id)

  if post_query.first() is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
  if post_query.first().user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Not authorized to perform requested action")
  
  post_query.update(post.dict(), synchronize_session=False)
  db.commit()

  return post_query.first()