from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from database import get_async_session
from utils.hasher import hash_password, verify_password
from utils import token
from auth.models import account
from auth import schemas
from auth import views

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
async def profile_register(user: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        """ User registration """
        user.hashed_password = hash_password(user.hashed_password)
        return await views.create_user(user.dict(), session)
    except IntegrityError:
        """ Handling 'Existing user' exception """
        raise HTTPException(status_code=404, detail="User already registered.")
    

@router.post("/login")
async def profile_login(format_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    """ Checking for user exist """
    user = await views.get_user(format_data.username, session)
    if user.get("data") == []:
        raise HTTPException(status_code=404, detail="User does not exists")
    user_data = user.get("data")[0]
    
    """ Password verifying """
    password = user_data.get("hashed_password")
    verified_password = verify_password(format_data.password, password)
    if not verified_password:
        raise HTTPException(status_code=404, detail="Incorrect email or password")
    
    """ Creating token """
    access_token_expires = token.timedelta(minutes=15)
    access_token = await token.create_access_token(
        data={"sub": format_data.username},
        expires_delta=access_token_expires,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {
            "email": user_data.get("email"),
            "username": user_data.get("username"),
        }
    }