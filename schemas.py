from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str
    author_id: int

class ShowBlog(BaseModel):
    title: str
    body: str
    author: "UserInfo"
    
class User(BaseModel):
    name: str
    email: str
    password:str

class UserInfo(BaseModel):
    name: str
    email: str

class UserLogin(BaseModel):
    email:str
    password: str    

class Token(BaseModel):
    access_token: str
    token_type: str
