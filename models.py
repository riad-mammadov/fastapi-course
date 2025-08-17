from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Blog(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str = Field(index = True)
    body: str
    author_id: int = Field(foreign_key="user.id") 
    author: "User" = Relationship(back_populates="blogs")

class User(SQLModel, table = True):
    id: int = Field(primary_key=True, index=True)
    name: str = Field(index = True)
    email: str
    password: str
    blogs: List[Blog] = Relationship(back_populates="author")


