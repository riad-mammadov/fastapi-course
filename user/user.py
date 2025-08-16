from schemas import User, UserInfo
from models import User as userModel
from fastapi import APIRouter, HTTPException,status
from database import SessionDep
from passlib.context import CryptContext

router = APIRouter(prefix="/user", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_pwd(password):
    return pwd_context.hash(password)

@router.post("/user", response_model=UserInfo)
def create_user(req:User, db:SessionDep):
    user_data = req.model_dump()
    user_data["password"] = hash_pwd(req.password)
    new_user =  userModel(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user/{id}", response_model=UserInfo)
def get_user(id: int, db:SessionDep):
    user = db.get(userModel, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with id of {id} not found")
    return user
    
