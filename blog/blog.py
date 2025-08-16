from fastapi import status, Response, HTTPException, APIRouter
from schemas import Blog as blogSchema, ShowBlog
from models import Blog as blogModel
from sqlmodel import select
from database import SessionDep
from typing import List

router = APIRouter(prefix="/blog", tags=["Blogs"])

@router.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}

@router.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(req:blogSchema, db: SessionDep):
    new_blog = blogModel(**req.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/blog", response_model=List[ShowBlog])
def all(db: SessionDep):
    blogs = db.exec(select(blogModel)).all()
    return blogs

@router.get("/blog/{id}", status_code=200, response_model=ShowBlog)
def specific(id:int, db: SessionDep, res:Response):
    blog = db.get(blogModel, id)
    if not blog:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {'error': f"Blog with ID of {id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with ID {id} not found.")
    return blog

@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int, db:SessionDep):
    blog = db.get(blogModel,id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()

@router.patch("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int, req:blogSchema, db:SessionDep):
    blog = db.get(blogModel, id)
    blog_data = req.model_dump(exclude_unset=True)
    blog.sqlmodel_update(blog_data)
    db.add(blog)
    db.commit()
    db.refresh(blog)
