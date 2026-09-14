from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.db.models import Post, User
from app.db.schemas import Post as PostSchema
from app.db.schemas import PostResponse
from app.dependencies import DbSession
from app.oauth2.utils import get_current_user

router = APIRouter(prefix="/posts", tags=["Post"])


@router.get("/", response_model=list[PostSchema])
# Need to pass db session as param
def get_all_post(
    db: DbSession,
    user: Annotated[User, Depends(get_current_user)],
):
    statement = select(Post).where(Post.user_id == user.id)
    data = db.scalars(statement).all()
    return data


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PostResponse,
)
def create_post(
    post: PostSchema,
    db: DbSession,
    user: Annotated[User, Depends(get_current_user)],
):
    # spreading the model data, spreading
    new_post = Post(user_id=user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{post_id}", response_model=PostResponse)
def get_post_by_id(
    post_id: int,
    db: DbSession,
    email: Annotated[str, Depends(get_current_user)],
):
    statement = select(Post).where(Post.id == post_id)

    data = db.scalar(statement)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return data


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(
    post_id: int,
    db: DbSession,
    user: Annotated[User, Depends(get_current_user)],
):
    statement = select(Post).where(Post.id == post_id, Post.user_id == user.id)
    data = db.scalar(statement)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(data)
    db.commit()


@router.put("/{post_id}", response_model=PostResponse)
def update_post_by_id(
    post_id: int,
    post: PostSchema,
    db: DbSession,
    user: Annotated[User, Depends(get_current_user)],
):
    statement = select(Post).where(Post.id == post_id, Post.user_id == user.id)

    data = db.scalar(statement)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    data.content = post.content
    data.title = post.title

    db.commit()
    db.refresh(data)

    return data
