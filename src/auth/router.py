from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from auth.models import account
from auth import schemas
from auth import views

router = APIRouter()

@router.post("/auth/register")
async def register(user: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        return await views.create_user(user.dict(), session)
    except:
        raise HTTPException(status_code=404, detail="User already registered.")