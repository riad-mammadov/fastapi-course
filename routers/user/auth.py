from passlib.context import CryptContext
from sqlmodel import select
from models import User as userModel
from fastapi import HTTPException, status
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os
import jwt
from jwt.exceptions import InvalidTokenError

load_dotenv()

JWT_SECRET: str = os.getenv("JWT_SECRET")
ALGORITHM = str = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_pwd(password):
    return pwd_context.hash(password)

def verify_pwd(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def auth_user(db, req):
    user = db.exec(select(userModel).where(userModel.email == req.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    hashed_password = user.password
    if not verify_pwd(req.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt