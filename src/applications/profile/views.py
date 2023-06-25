from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from applications.auth.models import account
from database import get_async_session


async def replenish_user_balance(credit: float, current_user: str, session: AsyncSession = Depends(get_async_session)):
    query = select(account).where(account.c.email == current_user)
    result = await session.execute(query)
    user_data = [dict(res._mapping) for res in result]
    balance = float(user_data[0].get("balance")) + credit
    stmt = (
        update(account).
        where(account.c.email == current_user).
        values(balance = balance)
    )
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success",
        "message": f"You've successfully replenished the balance. Your balance is {balance}"
    }
    
    
async def change_username(new_username: str, current_user: str, session: AsyncSession = Depends(get_async_session)):
    stmt = (
        update(account).
        where(account.c.email == current_user).
        values(username = new_username)
    )
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success",
        "message": "You've successfully changed username"
    }