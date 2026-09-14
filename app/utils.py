from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from argon2 import PasswordHasher
from pydantic import BaseModel
from sqlalchemy import select

from app.db.models import User
from app.dependencies import DbSession

ph = PasswordHasher()

SECRET_KEY = "e3d17ccb64a6e0338fc11537a3a0032d8f9a64557cd1915bbd43dec2e710b135"
EXPIRE_IN_MINS = 30
ALGORITHM = "HS256"


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=30)

    to_encode["exp"] = expire

    return jwt.encode(  # type: ignore
        payload=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )


def check_user_creds(db: DbSession, username: str, password: str):
    statement = select(User).where(User.email == username)
    db_user = db.scalar(statement)

    if not db_user:
        return False

    verify = ph.verify(password=password, hash=db_user.password)

    if not verify:
        return False

    return db_user
