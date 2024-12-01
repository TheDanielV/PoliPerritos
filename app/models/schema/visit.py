# app/models/schema/visit.py
from typing import Optional

from pydantic import BaseModel
from datetime import date

from app.models.schema.dog import AdoptedDogResponse


class VisitBase(BaseModel):
    visit_date: date
    evidence: str
    observations: Optional[str]


class VisitCreate(VisitBase):
    adopted_dog_id: int


class VisitResponse(VisitBase):
    id: int
    adopted_dog: AdoptedDogResponse

    class Config:
        from_attributes = True


class VisitUpdate(VisitBase):
    adopted_dog_id: int
    id: int
