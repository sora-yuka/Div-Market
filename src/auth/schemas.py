from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    email: str = Field(..., example="example@gmail.com")
    username: str = Field(..., example="example")
    hashed_password: str = Field(..., example="qwerty123")
    