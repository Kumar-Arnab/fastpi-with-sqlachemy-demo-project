from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

my_posts = []

class Post(BaseModel):
  title: str
  content: str
  #an optional fields with default set
  published: bool = True
  rating: Optional[int] = None

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
  return {"data": my_posts}

# title string, content string for post payload
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
  post_dict = post.dict()
  post_dict['id'] = len(my_posts)
  my_posts.append(post_dict)
  print(my_posts)
  # converting post model to dictionary
  return {"data": post}

# order matters in fastapi here latest can be treated as {id} so declaring it before
@app.get("/posts/latest")
def get_latest_post():
  post = my_posts[len(my_posts) - 1]
  return {"latest_post": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
  print(id)
  post = find_post(id)

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail= f"post with id {id} was not found")

  return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
  index = find_index_post(id)

  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} was not found")

  my_posts.pop(index)
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
  print(post)
  index = find_index_post(id)

  if index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id {id} was not found")
  
  post_dict = post.dict()
  post_dict["id"] = id
  my_posts[index] = post_dict
  return {"data": post_dict}