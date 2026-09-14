from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import jwt
from argon2 import PasswordHasher
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, ValidationError
from sqlalchemy import select
from sqlalchemy.orm import load_only

from app.db.models import User
from app.dependencies import DbSession

ph = PasswordHasher()

SECRET_KEY = "e3d17ccb64a6e0338fc11537a3a0032d8f9a64557cd1915bbd43dec2e710b135"
EXPIRE_IN_MINS = 30
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None
    email: EmailStr | None = None


def create_access_token(data: dict[str, Any]):
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


def verify_token(token: str, exception: HTTPException):
    try:
        payload = jwt.decode(  # type: ignore
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("id")
        email = payload.get("email")

        if user_id is None or email is None:
            raise exception

        return TokenData(id=user_id, email=email)

    except jwt.InvalidTokenError, ValidationError:
        raise exception


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DbSession,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token=token, exception=credentials_exception)

    statement = select(User).options(load_only(User.id)).where(User.id == token_data.id)
    db_user = db.scalar(statement)

    if not db_user:
        raise credentials_exception

    return db_user
