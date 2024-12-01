# app/models/schema/user.py
from typing import Optional

from pydantic import BaseModel
from app.models.domain.user import Role


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    role: Role


class UserResponse(UserBase):
    id: int
    role: Role
    is_active: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]

    class Config:
        from_attributes = True
