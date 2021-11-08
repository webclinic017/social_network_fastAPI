from typing import Optional
from psycopg2 import connect
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

from sqlalchemy.sql.functions import user

# from app.database import Base
# from app.routers.vote import vote


### Vote ###
class Vote(BaseModel):
    post_id: int
    dir: conint(le = 1)

### User ###
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


### Login ###
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None




### Post ###
class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    class Config:
        orm_mode = True