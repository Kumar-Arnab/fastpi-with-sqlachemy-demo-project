from pydantic import BaseModel

# class Post(BaseModel):
#   title: str
#   content: str
#   #an optional fields with default set
#   published: bool = True

# class CreatePost(BaseModel):
#   title: str
#   content: str
#   published: bool = True

# class UpdatePost(BaseModel):
#   title: str
#   content: str
#   published: bool

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

    