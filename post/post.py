from fastapi import APIRouter, status, HTTPException, Depends
from . import schemas
from datetime import datetime
from app.deps import authorize

post_router = APIRouter(
  prefix='/post',
  tags=['Post Methods']
)

@post_router.post('/', summary="Create new post")
async def create_post(request: schemas.PostBase, user: dict = Depends(authorize)):

  print(user)
  new_post = {
  image_url: request.image_url, 
  image_url_type: request.image_url_type,  
  caption: request.caption,
  creator_id: user.id,
  timestamp: datetime.now()  
  } 
  
  #get post data

  # Add user id to post creator

  # add post id to user post_ids
  return " "