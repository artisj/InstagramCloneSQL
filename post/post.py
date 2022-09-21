from fastapi import APIRouter, status, HTTPException, Depends
from . import schemas
from datetime import datetime
from app.deps import authorize
from db import db
from bson.json_util import dumps
from typing import List


post_router = APIRouter(
  prefix='/post',
  tags=['Post Methods']
)
image_url_types = ['absolute','relative']

@post_router.post('/', summary="Create new post")
async def create_post(request: schemas.PostBase, user: dict = Depends(authorize)):

  if not request.image_url_type in image_url_types:
    raise HTTPException(status_code=422, detail='Parameter image url type can only take values of absolute or relative.')
  
  new_post = {
  'image_url': request.image_url, 
  'image_url_type': request.image_url_type,  
  'caption': request.caption,
  'creator_id': user['id'],
  'timestamp': datetime.now(),
  'username': user['username']
  } 
  
  post_id = db.add_entry('post',new_post)
   
  # add post id to user
  db.update_user_post(post_id, user['id'])
  
  return new_post

@post_router.get('/list', summary="List posts", response_model=list[schemas.PostDisplay])
async def list_post():
  posts = list(db.list_posts())
  return posts