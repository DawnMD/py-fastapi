from typing import Annotated

from argon2 import PasswordHasher
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import DbSession
from app.oauth2.utils import Token, check_user_creds, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])
ph = PasswordHasher()


@router.post("/login", response_model=Token)
def login(user: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    valid_user = check_user_creds(username=user.username, password=user.password, db=db)

    if not valid_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    token = create_access_token({"email": valid_user.email, "id": valid_user.id})

    return Token(access_token=token, token_type="bearer")
