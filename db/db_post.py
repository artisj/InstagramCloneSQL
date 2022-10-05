from post.schemas import PostBase
from sqlalchemy.orm.session import Session
from db.models import DbPost
import datetime
from fastapi import HTTPException, status

def create_post(db: Session, request: PostBase):
  new_post = DbPost(
  image_url = request.image_url,
  image_url_type = request.image_url_type,
  caption = request.caption,
  timestamp = datetime.datetime.now(),
  user_id = request.creator_id
  )
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post


def view_posts(db: Session):
  return db.query(DbPost).all()

def delete(db: Session, post_id: int, user_id: int):
  post = db.query(DbPost).filter(DbPost.id == post_id).first()

  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    detail=f'Post with id {post_id} not found')

  if post.user_id != user_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    detail='Only post creator can delete post')
  
  db.delete(post)
  db.commit()
  return 'ok'
