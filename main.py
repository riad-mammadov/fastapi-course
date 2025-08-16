from fastapi import FastAPI
from schemas import Blog
from models import Blog as BlogModel
from database import engine
from sqlmodel import SQLModel
app = FastAPI()

SQLModel.metadata.create_all(engine)

@app.get('/')
def index():
    return {'data': 'blog list'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}

@app.get('/blog/{id}')
def show(id:int):
    return {'data': id}

@app.post("/blog")
def create_blog(req:Blog):
    return {'data': f"Blog Created with {req.title}"}

@app.get("/blog/{id}/comments")
def comments(id:str):
    return {'data': {'comments':'...'}}
