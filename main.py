import uvicorn
from fastapi import FastAPI
from user import user
from post import post
from app.settings import tags_metadata
from fastapi.staticfiles import StaticFiles
from routers import comment
from fastapi.middleware.cors import CORSMiddleware

from db.database import engine

from db import models


app = FastAPI(openapi_tags=tags_metadata)

app.mount('/images', StaticFiles(directory='images'), name='images')
app.include_router(user.user_router)
app.include_router(post.post_router)
app.include_router(comment.router)

origins = [
  'http://localhost:3000'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*']
)

@app.get('/')
async def home():
  return 'Home'

  
models.Base.metadata.create_all(engine)
#run on replit
uvicorn.run(app,host="0.0.0.0",port=8080)



#run from console
#uvicorn main:app --host="0.0.0.0"