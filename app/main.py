from fastapi import FastAPI
from .database import engine
from . import models, post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# routing all the request routes for post urls and user urls
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/") # this is called a decorator without this its not a fast api method
def root():
  return {"message": "welcome to fast api"}