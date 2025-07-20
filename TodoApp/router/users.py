from fastapi import APIRouter,Depends,Path,Query,HTTPException
from ..model import Todos
from ..model import Users
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import SessionLocal
from sqlalchemy.testing.pickleable import User
from starlette import status
from pydantic import BaseModel,Field
from .auth import get_current_user
from passlib.context import CryptContext
router = APIRouter(
prefix="/user",
    tags=["user"]
)

class User_verification(BaseModel):
    password: str
    new_password: str = Field(min_lenght=4)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency =  Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db : db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db.query(Todos).filter(Users.id == user.get('id')).all()

@router.put("/update_password",status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user:user_dependency,db : db_dependency , password_request:User_verification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(password_request.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    user_model.hashed_password = bcrypt_context.hash(password_request.new_password)
    db.add(user_model)
    db.commit()