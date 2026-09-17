import os
import secrets
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel


ENV_PATH = os.path.join(
    os.path.dirname(__file__),
    ".env"
)

load_dotenv(ENV_PATH)

SECRET = os.getenv("JWT_SECRET")

if not SECRET:
    raise RuntimeError("JWT_SECRET environment variable is not set")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class LoginRequest(BaseModel):
    username: str
    password: str


def authenticate_user(username: str, password: str):
    expected_username = os.getenv("AUTH_USERNAME")
    expected_password = os.getenv("AUTH_PASSWORD")

    if not expected_username or not expected_password:
        raise RuntimeError(
            "Authentication credentials are not configured"
        )

    if (
        secrets.compare_digest(username, expected_username)
        and secrets.compare_digest(password, expected_password)
    ):
        return True

    return False


def create_token(data: dict):
    to_encode = data.copy()

    to_encode["exp"] = (
        datetime.now(timezone.utc)
        + timedelta(hours=2)
    )

    return jwt.encode(
        to_encode,
        SECRET,
        algorithm="HS256"
    )


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )