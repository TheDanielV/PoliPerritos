# app/models/schema/course.py
from datetime import date
from typing import List

from pydantic import BaseModel

from app.models.schema.schedule import ScheduleCreate, ScheduleResponse


class CourseBase(BaseModel):
    name: str
    description: str
    start_date: date
    end_date: date
    price: float


class CourseCreate(CourseBase):
    schedule: List[ScheduleCreate]


class CourseUpdate(CourseBase):
    schedule: List[ScheduleCreate]


class CourseResponse(CourseBase):
    schedule: List[ScheduleResponse]
    id: int

    class Config:
        from_attributes = True
