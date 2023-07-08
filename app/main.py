from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import pymysql
import time

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

my_posts = []

class Post(BaseModel):
  title: str
  content: str
  #an optional fields with default set
  published: bool = True

def find_post(id):
  for p in my_posts:
    if p["id"] == id:
      return p
  return None

def find_index_post(id):
  for i, p in enumerate(my_posts):
    if p['id'] == id:
      return i
    
  return None

@app.get("/") # this is called a decorator without this its not a fast api method
def root():
  return {"message": "welcome to fast api"}

@app.get("/posts")
def get_posts():
  connection_new = None
  process_cursor = None
  try:
    connection_new = get_db_connection()
    with connection_new.cursor() as process_cursor:
      process_cursor.execute("""select * from posts;""")
      posts = process_cursor.fetchall()

      # print(posts)
      return {"data": posts}
  except Exception as e:
    print(e)
  finally:
    if process_cursor is not None:
      process_cursor.close()
    if connection_new is not None:
      connection_new.commit()
      connection_new.close()

# title string, content string for post payload
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
  connection_new = None
  process_cursor = None
  try:
    connection_new = get_db_connection()
    with connection_new.cursor() as process_cursor:
      process_cursor.execute("""insert into posts(`title`, `content`, `published`) values (%s, %s, %s)""", 
                 (post.title, post.content, post.published))
      process_cursor.execute("""select * from posts order by id desc limit 1;""")
      new_post = process_cursor.fetchone()

      # print(posts)
      return {"data": new_post}
  except Exception as e:
    print(e)
  finally:
    if process_cursor is not None:
      process_cursor.close()
    if connection_new is not None:
      connection_new.commit()
      connection_new.close()
  
  

# order matters in fastapi here latest can be treated as {id} so declaring it before
# @app.get("/posts/latest")
# def get_latest_post():
#   post = my_posts[len(my_posts) - 1]
#   return {"latest_post": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
  connection_new = None
  process_cursor = None
  try:
    connection_new = get_db_connection()
    with connection_new.cursor() as process_cursor:
      process_cursor.execute("""select * from posts where id = %s""", (id))
      post = process_cursor.fetchone()
      if post is None: 
        
        return {"detail": f"post with id {id} was not found"}
      return {"post_detail": post}
  except Exception as e:
    print(e)
  finally:
    if process_cursor is not None:
      process_cursor.close()
    if connection_new is not None:
      connection_new.commit()
      connection_new.close()


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  connection_new = None
  process_cursor = None
  try:
    connection_new = get_db_connection()
    with connection_new.cursor() as process_cursor:
      process_cursor.execute("""select * from posts where id = %s""", (id))
      post = process_cursor.fetchone()
      process_cursor.execute("""delete from posts where id = %s;""", (id))
      if post is None:
        return {"detail": f"post with id {id} was not found"}
      return Response(status_code=status.HTTP_204_NO_CONTENT)
  except Exception as e:
    print(e)
  finally:
    if process_cursor is not None:
      process_cursor.close()
    if connection_new is not None:
      connection_new.commit()
      connection_new.close()


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
  connection_new = None
  process_cursor = None
  try:
    connection_new = get_db_connection()
    with connection_new.cursor() as process_cursor:
      process_cursor.execute("""update posts set `title`=%s, `content`=%s, `published`=%s where id=%s""", 
                 (post.title, post.content, post.published, id))
      process_cursor.execute("""select * from posts where id=%s;""", id)
      new_post = process_cursor.fetchone()

      return {"data": new_post}
  except Exception as e:
    print(e)
  finally:
    if process_cursor is not None:
      process_cursor.close()
    if connection_new is not None:
      connection_new.commit()
      connection_new.close()