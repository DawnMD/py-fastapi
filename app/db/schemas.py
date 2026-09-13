# need to make a type class as we cannot use sqlalchemy class directly as type
from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
