from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import Blog
from models import Blog as blogModel
from database import engine
from sqlmodel import SQLModel, Session, select
from typing import Annotated


app = FastAPI()

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@app.get('/')
def index():
    return {'data': 'blog list'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}

@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(req:Blog, db: SessionDep):
    new_blog = blogModel(**req.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog")
def all(db: SessionDep):
    blogs = db.exec(select(blogModel)).all()
    return blogs

@app.get("/blog/{id}", status_code=200)
def specific(id:int, db: SessionDep, res:Response):
    blog = db.get(blogModel, id)
    if not blog:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': f"Blog with ID of {id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not found.")
    return blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteBlog(id:int, db:SessionDep):
    blog = db.get(blogModel,id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()

@app.patch("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id:int, req:Blog, db:SessionDep):
    blog = db.get(blogModel, id)
    blog_data = req.model_dump()
    blog.sqlmodel_update(blog_data)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    
    
    

