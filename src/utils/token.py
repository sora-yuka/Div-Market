import jwt
from jwt import PyJWTError
from pydantic import ValidationError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from applications.auth import schemas
from datetime import datetime, timedelta
from decouple import config


async def create_access_token(*, data: dict, expires_delta: timedelta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config("SECRET_KEY"), algorithm="HS256")


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(token, config("SECRET_KEY"), algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except (PyJWTError, ValidationError):
        raise credentials_exception
