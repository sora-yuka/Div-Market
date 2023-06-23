from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from tasks.tasks import send_email_confirmation, send_email_recovery
from random import randint
from database import get_async_session
from auth.models import account, code


async def get_user(email: str, session: AsyncSession = Depends(get_async_session)):
    """ Searching user by email """
    query = select(account).where(account.c.email == email)
    result = await session.execute(query)
    return {
        "status": "success",
        "data": [dict(res._mapping) for res in result]
    }
    
async def create_user(user: dict, session: AsyncSession = Depends(get_async_session)):
    """ Creating user with email sending """
    send_email_confirmation.delay(user.get("email"), user.get("activation_code"))
    stmt = insert(account).values(**user)
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success",
        "data": "We sent a verification letter to your email.",
        "detail": user
    }
    
async def activate_account(code: str, session: AsyncSession = Depends(get_async_session)):
    """ Activating user account """
    query = select(account).where(account.c.activation_code == code)
    result = await session.execute(query)
    data = [dict(res._mapping) for res in result]
    
    try:
        if data[0]:
            stmt = update(account).where(account.c.activation_code == code).values(is_active = True, activation_code = "")
            await session.execute(stmt)
            await session.commit()
        
            return {
                "status": "success",
                "data": "Account activated successfully!"
            }
    except IndexError:
        return {
            "status": "forbidden",
            "data": "Incorrect code, please try again."
        }

async def create_recovery_code(email: str, session: AsyncSession = Depends(get_async_session)):
    """ Creating recovery code to reset user password """
    recovery_code = randint(0000_0000, 9999_9999)
    send_email_recovery.delay(email, recovery_code)
    stmt = insert(code).values(email=email, code=recovery_code)
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success",
        "data": "We sent a recovery code, please check your email."
    }
    
async def set_new_password(email: str, recovery_code: int, new_password: str, session: AsyncSession = Depends(get_async_session)):
    query = select(code).where(code.c.email == email)
    result = await session.execute(query)
    user_data = {"data": [dict(res._mapping) for res in result]}.get("data")[0]
    user_email = user_data.get("email")
    user_recovery_code = user_data.get("code")
    if user_email != email and user_recovery_code != recovery_code:
        pass
    return "Good"