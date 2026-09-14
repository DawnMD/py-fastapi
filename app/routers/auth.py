from argon2 import PasswordHasher
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.db.models import User
from app.db.schemas import UserCreate
from app.dependencies import DbSession
from app.utils import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])
ph = PasswordHasher()


@router.post("/login")
def login(user: UserCreate, db: DbSession):
    statement = select(User).where(User.email == user.email)
    db_user = db.scalar(statement)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    verify = ph.verify(password=user.password, hash=db_user.password)

    if not verify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    token = create_access_token({"email": db_user.email})

    return token
