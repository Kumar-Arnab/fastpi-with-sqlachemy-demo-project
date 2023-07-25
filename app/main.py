from fastapi import FastAPI
from .database import engine
from . import models, post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# for cors errors for what domain could access our APIs
# "*" means a wildcard means any domain can access you APIs
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.co.in"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routing all the request routes for post urls and user urls
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/") # this is called a decorator without this its not a fast api method
def root():
  return {"message": "welcome to fast api"}