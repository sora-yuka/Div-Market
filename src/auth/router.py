from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from database import get_async_session
from utils.hasher import hash_password, verify_password
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
    result = await views.get_user(format_data.username, session)
    if result.get("data") == []:
        raise HTTPException(status_code=404, detail="User does not exists")
    password = result.get("data")[0].get("hashed_password")
    verified_password = verify_password(format_data.password, password)
    if not verified_password:
        raise HTTPException(status_code=404, detail="Incorrect email or password")
    return format_data