from pydantic import BaseModel, Field
from datetime import datetime


class UserRead(BaseModel):
    email: str
    username: str
    balance: float
    

class UserCreate(UserRead):
    hashed_password: str
    created_at: datetime = datetime.utcnow()