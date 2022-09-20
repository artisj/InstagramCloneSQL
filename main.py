import uvicorn
from fastapi import FastAPI
from user import user

tags_metadata = [{
                 'name': 'User Methods', 'description': 'Methods for users'
}]

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(user.user_router)

@app.get('/')
async def home():
  return 'Home'

#run on replit
uvicorn.run(app,host="0.0.0.0",port=8080)

#run from console
#uvicorn main:app --host="0.0.0.0"