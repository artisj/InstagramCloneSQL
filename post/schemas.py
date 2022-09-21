from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
  image_url: str #absoulte
  image_url_type: str  #relative or absolute
  caption: str
  

# for post display
class User(BaseModel):
  username: str

class PostDisplay(BaseModel):
  image_url: str #absoulte
  image_url_type: str  #relative or absolute
  caption: str
  timestamp: datetime
  username: str