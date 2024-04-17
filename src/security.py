from datetime import datetime, timedelta

from fastapi import Header, HTTPException, status
from jose import JWTError, jwt

from src.config import config


def create_access_token():
    payload = {
        "exp": datetime.utcnow()
        + timedelta(minutes=5)
        # we can add more data i.e. user_id, login_time, etc
    }

    encoded_jwt = jwt.encode(
        payload,
        config.AUTH_SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


# Dependency that validates the token from header.
# used with Depends()
def validate_token(token: str = Header(None)) -> bool | None:
    try:
        payload = jwt.decode(token, config.AUTH_SECRET_KEY, algorithms="HS256")
    except (JWTError, AttributeError):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token.")

    return True
