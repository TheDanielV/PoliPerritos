# app/models/domain/user.py
from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLAEnum
from sqlalchemy.orm import relationship

from app.db.database import Base


class Role(str, Enum):
    ADMIN = "admin"
    AUXILIAR = "auxiliar"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    role = Column(SQLAEnum(Role), nullable=False)
    is_active = Column(Boolean, default=True)

    # Relación uno-a-uno con el modelo Token
    token = relationship("AuthToken", uselist=False, back_populates="user")
