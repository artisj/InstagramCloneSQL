from pydantic import BaseModel, EmailStr


class User(BaseModel):
  
  email: EmailStr
  password: str
  
class Token(BaseModel):
  access_token: str


class TokenData(BaseModel):
  exp: int
  id: str
# auto add createdAt and UpdatedAt fields
