from pydantic import BaseModel
from datetime import datetime

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

class PostDisplay(BaseModel):
  image_url: str #absoulte
  image_url_type: str  #relative or absolute
  caption: str
  timestamp: datetime
  user: User
  class Config():
    orm_mode = True

