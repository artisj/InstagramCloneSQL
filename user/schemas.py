from pydantic import BaseModel, EmailStr


class User(BaseModel):
  username: str
  email: EmailStr
  password: str

class UserDisplay(BaseModel):
  username: str
  email: str
  
class Token(BaseModel):
  access_token: str

class TokenData(BaseModel):
  exp: int
  id: str
# auto add createdAt and UpdatedAt fields
