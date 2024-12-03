# app/models/domain/owner.py
from enum import Enum

from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, Enum as SQLAEnum
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.services.crypt import decrypt_str_data, encrypt_str_data


# Se crea el modelo paara un usuario
class Day(Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class Schedule(Base):
    __tablename__ = "schedule"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(SQLAEnum(Day), nullable=False)
    start_hour = Column(String(10), nullable=False)
    end_hour = Column(String(10), nullable=False)
    curso_id = Column(Integer, ForeignKey('course.id'))

    course = relationship("Course", back_populates="schedule")
