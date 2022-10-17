from datetime import datetime, timedelta

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from jwt import decode, encode, exceptions

from settings import Settings

settings = Settings()


def expire_date(days: int):
    date_expiration = datetime.now() + timedelta(days=days)
    return date_expiration


def write_token(data: dict):
    """Write token"""
    try:
        token = encode(
            payload={**data, "exp": expire_date(1)},
            key=settings.SECRET_TOKEN,
            algorithm=settings.TOKEN_ALGORITHM,
        )
        return token
    except HTTPException:
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content={
                "message": f"Error in token creation for user with email: {data['email']}"
            },
        )


def validate_token(token: str, output: bool = False):
    """Validate token"""
    try:
        if output:
            decoded = decode(
                token, key=settings.SECRET_TOKEN, algorithms=[settings.TOKEN_ALGORITHM]
            )
            return decoded
        decode(token, key=settings.SECRET_TOKEN, algorithms=[settings.TOKEN_ALGORITHM])
    except exceptions.DecodeError:
        return JSONResponse(status_code=401, content={"message": "Invalid token"})
    except exceptions.ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"message": "Token expired"})
