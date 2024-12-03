# app/models/schema/visit.py
from typing import Optional

from pydantic import BaseModel
from datetime import date

from app.models.schema.course import CourseResponse
from app.models.schema.dog import AdoptedDogResponse


class ApplicantBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    cellphone: str


class ApplicantCreate(ApplicantBase):
    course_id: int
    image: str


class ApplicantResponse(ApplicantBase):
    id: int
    course_id: int
    image: str

    class Config:
        from_attributes = True


class ApplicantUpdate(ApplicantBase):
    adopted_dog_id: int
    id: int
