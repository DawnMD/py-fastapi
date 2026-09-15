from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from app.db.models import Post, PostLike
from app.dependencies import DbSession
from app.oauth2.utils import get_current_user

router = APIRouter(tags=["Vote"], prefix="/vote")


class VoteIn(BaseModel):
    post_id: int
    vote_dir: Literal[1, 0]


@router.post("/", status_code=status.HTTP_201_CREATED)
def give_like(
    vote: VoteIn, user: Annotated[int, Depends(get_current_user)], db: DbSession
):
    post = db.get(Post, vote.post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )

    existing_like = db.scalar(
        select(PostLike).where(
            PostLike.post_id == vote.post_id,
            PostLike.user_id == user,
        )
    )

    # Like
    if vote.vote_dir == 1:
        if existing_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Post already liked",
            )

        like = PostLike(
            post_id=vote.post_id,
            user_id=user,
        )

        db.add(like)

    # Unlike
    else:
        if not existing_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Post is not liked",
            )

        db.delete(existing_like)

    db.commit()

    return {"message": "Post liked" if vote.vote_dir == 1 else "Post unliked"}
