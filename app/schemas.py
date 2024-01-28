from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    # rating:Optional[int] = True
class posts(Post):
    pass
    # owner_id:Optional[int] 
    
    
    
class UserCreate(BaseModel):
    email: EmailStr
    password:str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
class PostResponseModel(BaseModel):
    id:int
    title: str
    content: str
    published: bool = True
    owner_id:int
    owner:UserOut
    
    # class Config:
    #     orm_mode = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    
    
class PostOut(BaseModel):
    posts: PostResponseModel
    votes: int