from pydantic import BaseModel
from datetime import datetime

from typing import List

class PostBase(BaseModel):
  image_url: str #absoulte
  image_url_type: str  #relative or absolute
  caption: str
  creator_id: int

# for post display
class User(BaseModel):
  username: str
  class Config():
    orm_mode = True


# for post display
class Comment(BaseModel):
  text: str
  username: str
  timestamp: datetime
  class Config():
        orm_mode = True


class PostDisplay(BaseModel):
  image_url: str #absoulte
  image_url_type: str  #relative or absolute
  caption: str
  timestamp: datetime
  user: User
  comments: List[Comment]
  class Config():
    orm_mode = True

class CommentBase(BaseModel):
  username: str
  text: str
  post_id: int