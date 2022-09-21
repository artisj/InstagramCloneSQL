from fastapi import APIRouter, status, HTTPException, Depends
from . import schemas
from datetime import datetime
from app.deps import authorize
from db import db

post_router = APIRouter(
  prefix='/post',
  tags=['Post Methods']
)

@post_router.post('/', summary="Create new post")
async def create_post(request: schemas.PostBase, user: dict = Depends(authorize)):

  
  new_post = {
  'image_url': request.image_url, 
  'image_url_type': request.image_url_type,  
  'caption': request.caption,
  'creator_id': user['id'],
  'timestamp': datetime.now(),
  'username': user['username']
  } 
  
  #get post data
  
  post_id = db.add_entry('post',new_post)

  # add post id to user post_ids
  #db.update_entry('user',user['id'],str(post_id))
  
  
  return new_post

@post_router.get('/list', summary="List posts")
async def list_post():
  posts = db.list_posts()
  
  return posts