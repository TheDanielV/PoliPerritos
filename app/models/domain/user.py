# app/models/domain/user.py
from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLAEnum
from app.db.database import Base


class Role(str, Enum):
    ADMIN = "admin"
    AUXILIAR = "auxiliar"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(SQLAEnum(Role), index=True)
    is_active = Column(Boolean, default=True)
