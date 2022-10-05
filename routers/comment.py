from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_comment
from post.schemas import CommentBase
from app.deps import authorize

router = APIRouter(
  prefix='/comment',
  tags=['Comment Methods']
)

@router.get('all/{post_id}')
async def get_posts(post_id: int, db: Session = Depends(get_db)):
  return db_comment.get_all(db, post_id)

@router.post('')
def create(request: CommentBase, db: Session = Depends(get_db), user: dict = Depends(authorize)):
  return db_comment.create(db, request)