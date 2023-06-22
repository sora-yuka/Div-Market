from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from auth.models import account


async def check_user_exist(email: str, session: AsyncSession = Depends(get_async_session)):
    query = select(account).where(account.c.email == email)
    result = await session.execute(query)
    
    return {
        "status": "success",
        "data": [dict(res._mapping) for res in result]
    }

async def create_user(user: dict, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(account).values(**user)
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success"
    }