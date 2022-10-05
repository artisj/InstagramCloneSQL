from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .utils import (ALGORITHM, JWT_SECRET_KEY)

from jose import JWTError, jwt
from db import db_user

from db.database import get_db
from sqlalchemy.orm.session import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


async def authorize(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate your credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
  try:  
  
    payload = jwt.decode(token,JWT_SECRET_KEY,algorithms=ALGORITHM)
    id = payload.get("id")
    uname = str(payload.get("username"))
    
    if id is None:
      
      raise credentials_exception
          #token_data = TokenData(username=username)
  except Exception:
    raise credentials_exception
     
  user = db_user.get_user_by_username(db, uname)
  
  if user is None:
    print('user is none')
    raise credentials_exception
        
      
  return {'username': uname,'id': id}
