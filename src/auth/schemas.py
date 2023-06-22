from pydantic import BaseModel, Field
from datetime import datetime


class UserCreate(BaseModel):
    email: str = Field(..., example="example@gmail.com")
    username: str = Field(..., example="example")
    hashed_password: str = Field(..., example="qwerty123")
    created_at: datetime = datetime.utcnow()