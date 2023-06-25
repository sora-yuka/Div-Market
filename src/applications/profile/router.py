from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from applications.auth import schemas
from applications.auth.views import get_user
from utils.token import get_current_user

router = APIRouter(
    prefix="/api/v1/profile",
    tags=["Profile"],
)


@router.get("/")
async def get_active_user_profile(
        current_user: schemas.UserRead = Depends(get_current_user), 
        session: AsyncSession = Depends(get_async_session)
    ):
    user_data = await get_user(email=current_user, session=session)
    current_user = user_data.get("data")[0]
    if current_user.get("is_active") != True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive account")
    return current_user