# app/models/schema/dog.py
from datetime import date
from typing import Optional

from fastapi import UploadFile, File
from pydantic import BaseModel, Field
from app.models.schema.owner import OwnerBase, OwnerResponse
from app.models.domain.dog import Gender


# Schema for Abstract Dog
class DogBase(BaseModel):
    id: int
    name: str
    about: Optional[str]
    age: int
    is_vaccinated: bool
    image: Optional[str]
    gender: Gender


class DogCreate(DogBase):
    pass


class DogResponse(DogBase):
    class Config:
        orm_mode = True


# Schema for Static Dogs
class StaticDogBase(DogBase):
    pass


class StaticDogCreate(StaticDogBase):
    pass


class StaticDogResponse(StaticDogBase):
    class Config:
        orm_mode = True


# Schema for Adoption Dogs
class AdoptionDogBase(DogBase):
    pass


class AdoptionDogCreate(AdoptionDogBase):
    pass


class AdoptionDogResponse(AdoptionDogBase):
    class Config:
        orm_mode = True


# Schema for adopted dogs
class AdoptedDogBase(DogBase):
    adopted_date: date
    owner: OwnerBase


class AdoptedDogCreate(AdoptedDogBase):
    owner_id: int


class AdoptedDogResponse(BaseModel):
    id: int
    name: str
    about: Optional[str]
    age: int
    is_vaccinated: bool
    gender: Gender
    image: Optional[str]
    adopted_date: date
    owner: OwnerResponse

    class Config:
        orm_mode = True


