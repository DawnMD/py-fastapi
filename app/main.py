from argon2 import PasswordHasher
from fastapi import FastAPI, HTTPException, status
from sqlalchemy import select

from app.db.database import Base, engine
from app.db.models import Post, User
from app.db.schemas import Post as PostSchema
from app.db.schemas import UserBase, UserCreate
from app.dependencies import DbSession

app = FastAPI()
ph = PasswordHasher()
# To create the tables/ models from code
Base.metadata.create_all(engine)


@app.get("/posts")
# Need to pass db session as param
def get_all_post(db: DbSession):
    statement = select(Post)
    data = db.scalars(statement).all()
    return {"data": data}


@app.post("/post", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
def create_post(post: PostSchema, db: DbSession):
    # spreading the model data, spreading
    new_post = Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/post/{post_id}", response_model=PostSchema)
def get_post_by_id(post_id: int, db: DbSession):
    statement = select(Post).where(Post.id == post_id)

    data = db.scalar(statement)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return data


@app.delete("/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(post_id: int, db: DbSession):
    statement = select(Post).where(Post.id == post_id)
    data = db.scalar(statement)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(data)
    db.commit()


@app.put("/post/{post_id}", response_model=PostSchema)
def update_post_by_id(post_id: int, post: PostSchema, db: DbSession):
    statement = select(Post).where(Post.id == post_id)

    data = db.scalar(statement)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    data.content = post.content
    data.title = post.title

    db.commit()
    db.refresh(data)

    return data


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserBase)
def create_user(user: UserCreate, db: DbSession):

    # hash password first

    hash = ph.hash(user.password)
    user.password = hash

    statement = User(**user.model_dump())
    db.add(statement)
    db.commit()
    db.refresh(statement)

    return statement


@app.get("/users/{user_id}", response_model=UserBase)
def get_user_by_id(user_id: int, db: DbSession):
    statement = select(User).where(User.id == user_id)
    data = db.scalar(statement)

    return data
