from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from tasks.tasks import send_email_confirmation
from database import get_async_session
from auth.models import account


async def get_user(email: str, session: AsyncSession = Depends(get_async_session)):
    query = select(account).where(account.c.email == email)
    result = await session.execute(query)
    
    return {
        "status": "success",
        "data": [dict(res._mapping) for res in result]
    }

async def create_user(user: dict, session: AsyncSession = Depends(get_async_session)):
    """ Creating user with email sending """
    send_email_confirmation.delay(user.get("email"))
    stmt = insert(account).values(**user)
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success",
        "data": "We sent a verification letter to your email.",
        "detail": user
    }