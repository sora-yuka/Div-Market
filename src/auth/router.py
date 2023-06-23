import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from random import randint
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
        user.activation_code = str(uuid.uuid4())
        user.hashed_password = hash_password(user.hashed_password)
        return await views.create_user(user.dict(), session)
    except IntegrityError:
        """ Handling 'existing user' exception """
        raise HTTPException(status_code=404, detail="User already registered.")
    
    
@router.post("/confirm")
async def profile_activation(activation_code: str, session: AsyncSession = Depends(get_async_session)):
    """ Account activation """
    user_data = await views.activate_account(activation_code, session)
    return user_data
    

@router.post("/login")
async def profile_login(format_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    """ Checking for user exist """
    user = await views.get_user(format_data.username, session)
    if user.get("data") == []:
        raise HTTPException(status_code=404, detail="User does not exists.")
    user_data = user.get("data")[0]
    
    """ Password verifying """
    password = user_data.get("hashed_password")
    verified_password = verify_password(format_data.password, password)
    if not verified_password:
        raise HTTPException(status_code=404, detail="Incorrect email or password.")
    
    if user_data.get("is_active") == True:
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
    return {
        "status": "forbidden",
        "data": "Account doesn't activated."
    }
    
@router.post("/forgot-password")
async def profile_recovery(request: schemas.ForgotPassword, session: AsyncSession = Depends(get_async_session)):
    """ Checking for user exist """
    user_data = await views.get_user(request.email, session)
    try:
        if user_data.get("data")[0]:
            return await views.create_recovery_code(request.email, session)
    except IndexError:
        raise HTTPException(status_code=404, detail="User does not exists.")
    except IntegrityError:
        raise HTTPException(status_code=404, detail="We have sent a recovery code, check your email or resend code.")
    

@router.post("/password-recovery")
async def profile_set_new_password(request: schemas.PasswordRecovery, session: AsyncSession = Depends(get_async_session)):
    # try:
    return await views.set_new_password(
        email=request.email, recovery_code=request.recovery_code, 
        new_password=request.new_password, session=session
    )
    # except:
    #     return "something get wrong"