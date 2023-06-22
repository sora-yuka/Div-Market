from fastapi import APIRouter, Depends, HTTPException
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
    
@router.get("/profile")
async def get_profile(email: str, session: AsyncSession = Depends(get_async_session)):
    return await views.get_user(email, session)