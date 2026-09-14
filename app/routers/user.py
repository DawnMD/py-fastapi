from argon2 import PasswordHasher
from fastapi import APIRouter, status
from sqlalchemy import select

from app.db.models import User
from app.db.schemas import UserBase, UserCreate
from app.dependencies import DbSession

ph = PasswordHasher()

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserBase)
def create_user(user: UserCreate, db: DbSession):

    # hash password first

    hash = ph.hash(user.password)
    user.password = hash

    statement = User(**user.model_dump())
    db.add(statement)
    db.commit()
    db.refresh(statement)

    return statement


@router.get("/{user_id}", response_model=UserBase)
def get_user_by_id(user_id: int, db: DbSession):
    statement = select(User).where(User.id == user_id)
    data = db.scalar(statement)

    return data
