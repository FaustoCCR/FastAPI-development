from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


# * reading model
class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# * Authentication
class UserLogin(UserCreate):
    ...
