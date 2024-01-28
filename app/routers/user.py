from .. import models,schemas
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserCreate,UserOut
from fastapi import FastAPI,status,Depends,APIRouter
from ..models import User
from ..utilities import hashed

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    hash_pass = hashed(user.password)
    user.password = hash_pass
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user