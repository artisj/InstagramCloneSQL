from fastapi import HTTPException,status
from user.schemas import User
from sqlalchemy.orm.session import Session
from db.models import DbUser
from app.utils import get_hashed_password

def create_user(db: Session, request: User):
  new_user = DbUser(
  username = request.username,
  email = request.email,
  password = get_hashed_password(request.password)
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def view_users(db: Session):
  return db.query(DbUser).all()

def user_login(db: Session,request: User):
  pass

def get_user_by_username(db: Session, username: str):
  user = db.query(DbUser).filter(DbUser.username == username).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
     detail=f'User with username {username} not found')
  return user