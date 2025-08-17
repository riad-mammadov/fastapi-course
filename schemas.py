from pydantic import BaseModel
from typing import List

class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(BaseModel):
    title: str
    author_id: int
    
class User(BaseModel):
    name: str
    email: str
    password:str

class UserInfo(BaseModel):
    name: str
    blogs: List[Blog]

    