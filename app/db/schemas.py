# need to make a type class as we cannot use sqlalchemy class directly as type
from datetime import datetime

from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: datetime


class PostResponse(Post):
    user_id: int


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
