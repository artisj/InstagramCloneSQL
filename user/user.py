from fastapi import APIRouter, status, HTTPException, Depends

#from app.schemas import UserOut, UserAuth
from . import schemas
#from db import db
from app.utils import get_hashed_password
from app.deps import authorize
from datetime import datetime

from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user

from fastapi.security import OAuth2PasswordRequestForm
from app import utils

from db.models import DbUser


user_router = APIRouter(
  prefix='/user',
  tags=['User Methods']
)

@user_router.post('/signup', summary="Create new user", response_model=schemas.UserDisplay)
# async def create_user(data: schemas.User):   # setup for mongodb
    # querying database to check if user already exist
    # user = db.get_user_by('user', 'email', data.email)
    # if user is not None:
    #         raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="User with this email already exist"
    #     )
    # user = {
    #     'username': data.username,
    #     'email': data.email,
    #     'password': get_hashed_password(data.password),
    #     'created': datetime.today()
    # }
    # db.add_entry('user',user)   # saving user to database
    # return user

async def create_user(request: schemas.User, db: Session = Depends(get_db)):
  return db_user.create_user(db,request)
  
@user_router.get('/users')
async def see_users(db: Session = Depends(get_db)):
  return db_user.view_users(db)

# formdata has to be called username for input not email
@user_router.post('/login', summary="Create access token for user", response_model=schemas.Token)
async def login(request: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.password
    if not utils.verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": utils.create_access_token({ 'id': user.id,'username': user.username})
    }

# add dependency get_current_user to protect route
@user_router.get("/users/me/")
async def read_users_me(user: dict = Depends(authorize),db: Session = Depends(get_db)):
    return db_user.get_user_by_username(db, user.username)
