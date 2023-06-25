import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from random import randint
from database import get_async_session
from utils.token import get_current_user, create_access_token
from utils.hasher import hash_password, verify_password
from applications.auth.models import account
from applications.auth import schemas
from datetime import timedelta
from applications.auth import views

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)

@router.post("/register")
async def profile_register(user: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    """ User registration """
    try:
        # creating user activation code
        user.activation_code = str(uuid.uuid4())
        # hashing user password
        user.hashed_password = hash_password(password=user.hashed_password)
        # creating user in database
        return await views.create_user(user.dict(), session)
    except IntegrityError:
        """ Handling 'existing user' exception """
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User already registered.")
    
    
@router.post("/confirm")
async def profile_activation(activation_code: str, session: AsyncSession = Depends(get_async_session)):
    """ Account activation """
    user_data = await views.activate_account(code=activation_code, session=session)
    return user_data
    

@router.post("/login")
async def profile_login(format_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    """ Checking for user exist """
    # getting user data
    try:
        """ Password verifying """
        user_data = await views.get_user(email=format_data.username, session=session)
        password = user_data.get("data").get("hashed_password")
        # validating of the user's password
        verified_password = verify_password(plain_password=format_data.password, hashed_password=password)
        if not verified_password:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password.")
        
        if user_data.get("data").get("is_active") == True:
            """ Creating token """
            access_token_expires = timedelta(minutes=15)
            access_token = await create_access_token(
                data={"sub": format_data.username},
                expires_delta=access_token_expires,
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_info": {
                    "email": user_data.get("data").get("email"),
                    "username": user_data.get("data").get("username"),
                }
            }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inactive account.")
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists.")
    
    
@router.post("/forgot-password")
async def profile_recovery(request: schemas.ForgotPassword, session: AsyncSession = Depends(get_async_session)):
    """ Checking for user exist """
    # getting user data
    try:
        """ Creating recovery code """
        user_data = await views.get_user(email=request.email, session=session)
        # if user_data.get("data"):
        # generating recovery code for password reset
        return await views.create_recovery_code(email=request.email, session=session)
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists.")
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="We have sent a recovery code, check your email or resend code."
        )


@router.post("/password-recovery")
async def profile_set_new_password(
        request: schemas.PasswordRecovery, 
        session: AsyncSession = Depends(get_async_session)
    ):
    """ Updating user password """
    return await views.set_new_password(
        email=request.email, recovery_code=request.recovery_code, 
        new_password=hash_password(request.new_password), session=session
    )
    

@router.post("/password-change")
async def profile_password_change(
        request: schemas.PasswordChange,
        current_user: schemas.UserRead = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
    ):
    """ Changing user password """
    # getting user data
    try:
        user_data = await views.get_user(email=current_user, session=session)
        user_data = user_data.get("data")
        if user_data.get("is_active") == True:
            old_password = user_data.get("hashed_password")
            # validating of the user's old password
            veryfied_password = verify_password(plain_password=request.old_password, hashed_password=old_password)
            if not veryfied_password:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Old password mismatch.")
            # changing of the user's password
            return await views.change_password(
                current_user=current_user, old_password=request.old_password,
                new_password=hash_password(password=request.new_password), session=session
            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not activated.")
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect email.")