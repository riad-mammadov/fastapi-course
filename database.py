from sqlmodel import create_engine

db = 'sqlite:///./blog.db'
engine = create_engine(db, connect_args={"check_same_thread": False})



