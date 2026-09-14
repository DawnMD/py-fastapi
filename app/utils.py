from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pydantic import BaseModel

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
