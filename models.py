from sqlmodel import SQLModel, Field

class Blog(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str = Field(index = True)
    body: str
    author_id: str = Field(default=None, foreign_key="user.id")

class User(SQLModel, table = True):
    id: int = Field(primary_key=True, index=True)
    name: str = Field(index = True)
    email: str
    password: str

