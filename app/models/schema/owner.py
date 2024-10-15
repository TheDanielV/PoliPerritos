# app/models/schema/owner.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from app.models.schema.dog import DogResponse


class OwnerBase(BaseModel):
    name: str
    direction: str
    cellphone: int


class OwnerCreate(OwnerBase):
    pass


class OwnerResponse(OwnerBase):
    id: int

    class Config:
        orm_mode = True
