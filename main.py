from fastapi import FastAPI, Depends
from database import engine
from sqlmodel import SQLModel, Session
from routers.blog.blog import router as blogRouter
from routers.user.user import router as userRouter

app = FastAPI()

SQLModel.metadata.create_all(engine)


app.include_router(blogRouter)
app.include_router(userRouter)

@app.get('/')
def index():
    return {'data': 'blog list'}


    

