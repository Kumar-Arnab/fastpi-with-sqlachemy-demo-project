from fastapi import Response, status, HTTPException, Depends, APIRouter
from .schemas import PostCreate, Post
from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
  prefix="/posts",
  tags=['Posts']
)
# by mentioning the '/posts' we can remove the posts from every single api router.get with a simple '/'

# API to fetch all posts
@router.get("/", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
  posts = db.query(models.Post).all()

  return posts

# title string, content string for post payload
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  # retrieve the new_post and store it in new_post variable
  db.refresh(new_post)

  return new_post

@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id).first()

  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")

  return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  post_query = db.query(models.Post).filter(models.Post.id == id)

  if post_query.first() is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
  post_query.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
  post_query = db.query(models.Post).filter(models.Post.id == id)

  if post_query.first() is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
  post_query.update(post.dict(), synchronize_session=False)
  db.commit()

  return post_query.first()