from fastapi import Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from tasks.tasks import send_email_confirmation, send_email_recovery
from random import randint
from database import get_async_session
from applications.auth.models import account, code


async def get_user(email: str, session: AsyncSession = Depends(get_async_session)):
    """ Searching user in database by email """
    query = select(account).where(account.c.email == email)
    result = await session.execute(query)
    user_data = [dict(res._mapping) for res in result]
    return {
        "status": "success",
        "data": user_data[0]
    }
    
async def create_user(user: dict, session: AsyncSession = Depends(get_async_session)):
    """ Creating user with email sending """
    send_email_confirmation.delay(user.get("email"), user.get("activation_code"))
    stmt = insert(account).values(**user)
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success",
        "message": "We've sent a verification letter to your email.",
        "data": user
    }
    
async def activate_account(code: str, session: AsyncSession = Depends(get_async_session)):
    """ Activating user account """
    query = select(account).where(account.c.activation_code == code)
    result = await session.execute(query)
    user_data = [dict(res._mapping) for res in result]
    
    try:
        user_data = user_data[0]
        stmt = (
            update(account).
            where(account.c.activation_code == code).
            values(is_active = True, activation_code = "")
        )
        await session.execute(stmt)
        await session.commit()
    
        return {
            "status": "success",
            "message": "Account activated successfully!"
        }
    except IndexError:
        return {
            "status": "forbidden",
            "message": "Incorrect code, please try again."
        }

async def create_recovery_code(email: str, session: AsyncSession = Depends(get_async_session)):
    """ Creating recovery code to reset user password """
    user_data = await get_user(email=email, session=session)
    user_data = user_data.get("data")
    recovery_code = randint(0000_0000, 9999_9999)
    send_email_recovery.delay(email, recovery_code)
    stmt = insert(code).values(email=email, code=recovery_code)
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success",
        "message": "We've sent a recovery code, please check your email."
    }
    
async def set_new_password(
        email: str, recovery_code: int, new_password: str, 
        session: AsyncSession = Depends(get_async_session)
    ):
    """ Seting the user's new password """
    query = select(code).where(code.c.email == email)
    result = await session.execute(query)
    
    try:
        user_data = {"data": [dict(res._mapping) for res in result]}.get("data")
        user_recovery_code = user_data[0].get("code")
        if user_recovery_code != recovery_code:
            return {
                "status": "forbidden",
                "message": "Incorrect code.",
            }
        stmt = (
            update(account).
            where(account.c.email == email).
            values(hashed_password = new_password)
        )
        await session.execute(stmt)
        await session.commit()
        stmt = delete(code).where(code.c.email == email)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "message": "Password has been reset successfully."
        }
    except IndexError:
        return {
            "status": "forbidden",
            "message": "Incorrect email or you've already reset your password. Please, click on 'send recovery code'."
        }
        

async def change_password(
        current_user: str, old_password: str, new_password: str, 
        session: AsyncSession = Depends(get_async_session)
    ):
    """ Changing the user's old password """
    user_data = await get_user(email=current_user, session=session)
    user_data = user_data.get("data")
    stmt = (
        update(account).
        where(account.c.email == current_user).
        values(hashed_password = new_password)
    )
    await session.execute(stmt)
    await session.commit()
    return {
        "status": "success",
        "message": "Password has been updated successfully."
    }