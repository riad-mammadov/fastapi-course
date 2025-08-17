from sqlmodel import create_engine
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

db = 'sqlite:///./blog.db'
engine = create_engine(db, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

