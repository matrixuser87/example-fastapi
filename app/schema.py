from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
