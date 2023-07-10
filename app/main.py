from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from .schemas import PostCreate
import pymysql
import time
from .database import engine, get_db
from . import models
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

db_host_name = "localhost"
db_user_name = "root"
db_user_password = "Vivasva@20"
db_schema_name = "fastapi"

def get_db_connection():
  connection = None
  try:
    connection = pymysql.connect(db= db_schema_name,
                                 user= db_user_name,
                                 passwd= db_user_password,
                                 host= db_host_name)
    
    if connection is not None:
      print("Connection is successful")
  except Exception as exception:
    print(f"Connection not successful {exception}")
  
  return connection

app = FastAPI()

@app.get("/") # this is called a decorator without this its not a fast api method
def root():
  return {"message": "welcome to fast api"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

  # here db is dependency object which creates a db session with the method get_db()
  posts = db.query(models.Post).all()

  return {"data": posts}

# API to fetch all posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
  # connection_new = None
  # process_cursor = None
  # try:
  #   connection_new = get_db_connection()
  #   with connection_new.cursor() as process_cursor:
  #     process_cursor.execute("""select * from posts;""")
  #     posts = process_cursor.fetchall()

  #     # print(posts)
  #     return {"data": posts}
  # except Exception as e:
  #   print(e)
  # finally:
  #   if process_cursor is not None:
  #     process_cursor.close()
  #   if connection_new is not None:
  #     connection_new.commit()
  #     connection_new.close()

  # now using sql alchemy
  posts = db.query(models.Post).all()

  return {"data": posts}

# title string, content string for post payload
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
  # connection_new = None
  # process_cursor = None
  # try:
  #   connection_new = get_db_connection()
  #   with connection_new.cursor() as process_cursor:
  #     process_cursor.execute("""insert into posts(`title`, `content`, `published`) values (%s, %s, %s)""", 
  #                (post.title, post.content, post.published))
  #     process_cursor.execute("""select * from posts order by id desc limit 1;""")
  #     new_post = process_cursor.fetchone()

  #     # print(posts)
  #     return {"data": new_post}
  # except Exception as e:
  #   print(e)
  # finally:
  #   if process_cursor is not None:
  #     process_cursor.close()
  #   if connection_new is not None:
  #     connection_new.commit()
  #     connection_new.close()

  # **post.dict() -> title=post.title, content=post.content, published=post.published
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  # retrieve the new_post and store it in new_post variable
  db.refresh(new_post)

  return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
  # connection_new = None
  # process_cursor = None
  # try:
  #   connection_new = get_db_connection()
  #   with connection_new.cursor() as process_cursor:
  #     process_cursor.execute("""select * from posts where id = %s""", (id))
  #     post = process_cursor.fetchone()
  #     if post is None: 
        
  #       return {"detail": f"post with id {id} was not found"}
  #     return {"post_detail": post}
  # except Exception as e:
  #   print(e)
  # finally:
  #   if process_cursor is not None:
  #     process_cursor.close()
  #   if connection_new is not None:
  #     connection_new.commit()
  #     connection_new.close()

  post = db.query(models.Post).filter(models.Post.id == id).first()

  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")

  return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  # connection_new = None
  # process_cursor = None
  # try:
  #   connection_new = get_db_connection()
  #   with connection_new.cursor() as process_cursor:
  #     process_cursor.execute("""select * from posts where id = %s""", (id))
  #     post = process_cursor.fetchone()
  #     process_cursor.execute("""delete from posts where id = %s;""", (id))
  #     if post is None:
  #       return {"detail": f"post with id {id} was not found"}
  #     return Response(status_code=status.HTTP_204_NO_CONTENT)
  # except Exception as e:
  #   print(e)
  # finally:
  #   if process_cursor is not None:
  #     process_cursor.close()
  #   if connection_new is not None:
  #     connection_new.commit()
  #     connection_new.close()

  post_query = db.query(models.Post).filter(models.Post.id == id)

  if post_query.first() is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
  post_query.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
  # connection_new = None
  # process_cursor = None
  # try:
  #   connection_new = get_db_connection()
  #   with connection_new.cursor() as process_cursor:
  #     process_cursor.execute("""update posts set `title`=%s, `content`=%s, `published`=%s where id=%s""", 
  #                (post.title, post.content, post.published, id))
  #     process_cursor.execute("""select * from posts where id=%s;""", id)
  #     new_post = process_cursor.fetchone()

  #     return {"data": new_post}
  # except Exception as e:
  #   print(e)
  # finally:
  #   if process_cursor is not None:
  #     process_cursor.close()
  #   if connection_new is not None:
  #     connection_new.commit()
  #     connection_new.close()

  post_query = db.query(models.Post).filter(models.Post.id == id)

  if post_query.first() is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")
  
  post_query.update(post.dict(), synchronize_session=False)
  db.commit()

  return {"data": post_query.first()}