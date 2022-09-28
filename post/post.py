from fastapi import APIRouter, status, HTTPException, Depends, UploadFile, File
from . import schemas
from datetime import datetime
from app.deps import authorize
from db import db
from bson.json_util import dumps
from typing import List
import random
import string
import shutil

from db import db_post
from db.database import get_db
from sqlalchemy.orm.session import Session

post_router = APIRouter(
  prefix='/post',
  tags=['Post Methods']
)
image_url_types = ['absolute','relative']

@post_router.post('', summary="Create new post")
# async def create_post(request: schemas.PostBase, user: dict = Depends(authorize)):
async def create(request: schemas.PostBase, user: dict = Depends(authorize), db: Session = Depends(get_db)):
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
  
  # post_id = db.add_entry('post',new_post)
   
  # add post id to user
  # db.update_user_post(post_id, user['id'])
  
  return db_post.create(db, request)

@post_router.get('/list', summary="List posts", response_model=List[schemas.PostDisplay])
async def list_post():
  posts = list(db.list_posts())
  return posts

@post_router.post('/image', summary='Upload an image for post')
async def upload_image(image: UploadFile = File(...),user: dict = Depends(authorize)):
  letters = string.ascii_letters
  #random string for filename
  rand_str = ''.join(random.choice(letters) for i in range(6))
  new = f'_{rand_str}.'
  filename = new.join(image.filename.rsplit('.',1))
  path = f'images/{filename}'

  with open(path, 'w+b') as buffer:
    shutil.copyfileobj(image.file, buffer)

  return {'filename': path}

@post_router.delete('/delete/{id}', summary='Delete post')
async def delete_post(id: str,user: dict = Depends(authorize)):
  if not id:
    raise HTTPException(status_code=404, detail='Post not found.')
  
  username = db.get_post_user(id)
  print(username)
  if username == None:
    raise HTTPException(status_code=404, detail='Post not found for user') 

  if username != user['username']:
    raise HTTPException(status_code=403, detail='Post matches another user') 
    
  # delete post from post  
  db.delete('post',id)

  # delete id from user
  db.delete_post_from_user(id,user['id'])
  return {'detail': f'Post {id} deleted'}