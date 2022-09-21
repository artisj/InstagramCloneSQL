import uvicorn
from fastapi import FastAPI
from user import user
from post import post
from app.settings import tags_metadata



app = FastAPI(openapi_tags=tags_metadata)


app.include_router(user.user_router)
app.include_router(post.post_router)

@app.get('/')
async def home():
  return 'Home'

#run on replit
uvicorn.run(app,host="0.0.0.0",port=8080)

#run from console
#uvicorn main:app --host="0.0.0.0"