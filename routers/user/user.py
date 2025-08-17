from schemas import User, UserInfo, UserLogin, Token
from models import User as userModel
from fastapi import APIRouter, HTTPException,status, Depends
from database import SessionDep
from .auth import hash_pwd, auth_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token,ALGORITHM, JWT_SECRET
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from dotenv import load_dotenv
from datetime import timedelta
import jwt
from jwt import InvalidTokenError
from sqlmodel import select

router = APIRouter(prefix="/user", tags=["Users"])

bearer_scheme = HTTPBearer(bearerFormat="JWT")

def get_current_user(db: SessionDep, token: str = Depends(bearer_scheme)):
    try:
        payload = jwt.decode(token.credentials, JWT_SECRET, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.exec(select(userModel).where(userModel.email == user_email)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.delete("/delete", status_code=200)
def delete_account(db: SessionDep, req: User = Depends(get_current_user)):
    db.delete(req)
    db.commit()
    return {"detail": "Your account has been deleted"}

@router.post("/", response_model=UserInfo)
def create_user(req:User, db:SessionDep):
    user_data = req.model_dump()
    user_data["password"] = hash_pwd(req.password)
    new_user =  userModel(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserInfo)
def get_user(id: int, db:SessionDep):
    user = db.get(userModel, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id of {id} not found")
    return user

@router.post("/login")
def login(req:UserLogin, db:SessionDep):
    user = auth_user(db, req)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")