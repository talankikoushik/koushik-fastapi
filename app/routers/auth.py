from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas import UserLogin,Token
from ..database import get_db
from ..models import User
from ..utilities import verify
from .. import oauth2

router = APIRouter(tags = ['Authentication'])


# @router.post('/login')
# def create_user(user_credentials:UserLogin, db:Session =Depends(get_db)):
#     users = db.query(User).filter(User.email == user_credentials.email).first()
#     if not users:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
#     if not verify(user_credentials.password, users.password):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        
#     access_token = oauth2.create_access_token(data={"user_id": users.id}) #payload data={"user_id": user.id} 

#     return {"access_token": access_token, "token_type": "bearer"}


@router.post('/login', response_model=Token)
def create_user(user_credentials: OAuth2PasswordRequestForm= Depends(), db:Session =Depends(get_db)):
    users = db.query(User).filter(User.email == user_credentials.username).first()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not verify(user_credentials.password, users.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        
    access_token = oauth2.create_access_token(data={"user_id": users.id}) #payload data={"user_id": user.id} 

    return {"access_token": access_token, "token_type": "bearer"}
