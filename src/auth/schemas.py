from pydantic import BaseModel, Field
from datetime import datetime


class UserRead(BaseModel):
    email: str
    username: str
    balance: float
    activation_code: str = None
    

class UserCreate(UserRead):
    hashed_password: str
    created_at: datetime = datetime.utcnow()
    

class ForgotPassword(BaseModel):
    email: str
    

class PasswordRecovery(ForgotPassword):
    recovery_code: int
    new_password: str
    
    
class PasswordChange(ForgotPassword):
    old_password: str
    new_password: str
    