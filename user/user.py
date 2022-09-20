from fastapi import APIRouter, status, HTTPException, Depends

#from app.schemas import UserOut, UserAuth
from . import schemas
from db import db
from app.utils import get_hashed_password
from app.deps import authorize
from datetime import datetime

from fastapi.security import OAuth2PasswordRequestForm
from app import utils

user_router = APIRouter()

@user_router.post('/signup', summary="Create new user",tags=['User Methods'], response_model=schemas.User)
async def create_user(data: schemas.User):
    # querying database to check if user already exist
    user = db.get_user_by('user', 'email', data.email)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = {
        'email': data.email,
        'password': get_hashed_password(data.password),
        'created': datetime.today()
    }
    db.add_entry('user',user)   # saving user to database
    return { 'detail': f'{user.email} has be registered'}

# formdata has to be called username for input not email
@user_router.post('/login', summary="Create access token for user",tags=['User Methods'], response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.get_user_by('user','email', form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user['password']
    if not utils.verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": utils.create_access_token(user['_id'])
    }

# add dependency get_current_user to protect route
@user_router.get("/users/me/", response_model=str)
async def read_users_me(id: str = Depends(authorize)):
    return id
#aj@gmail.com
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjE4ODUzNzcsImlkIjoiNjMwZTI3MGFhMWI2MmFhNmY4NDM3MDAwIn0.cZjD-03pNzhoV9tJTJQe54pTzoYxO3Mk3oGKLvgFs18