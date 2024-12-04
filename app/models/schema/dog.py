# app/models/schema/dog.py
from datetime import date
from typing import Optional

from fastapi import UploadFile, File
from pydantic import BaseModel, Field
from app.models.schema.owner import OwnerBase, OwnerResponse
from app.models.domain.dog import Gender


# Schema for Abstract Dog
class DogBase(BaseModel):
    id_chip: Optional[int]
    name: str
    about: Optional[str]
    age: int
    is_vaccinated: bool
    image: Optional[str]
    gender: Gender
    entry_date: Optional[date]
    is_sterilized: bool
    is_dewormed: bool
    operation: Optional[str]


class DogCreate(DogBase):
    pass


class DogResponse(DogBase):
    class Config:
        from_attributes = True


# Schema for Static Dogs
class StaticDogBase(DogBase):
    pass


class StaticDogCreate(StaticDogBase):
    pass


class StaticDogResponse(StaticDogBase):
    id: int

    class Config:
        from_attributes = True


# Schema for Adoption Dogs
class AdoptionDogBase(DogBase):
    pass


class AdoptionDogCreate(AdoptionDogBase):
    pass


class AdoptionDogResponse(AdoptionDogBase):
    id: int

    class Config:
        from_attributes = True


# Schema for adopted dogs
class AdoptedDogBase(DogBase):
    adopted_date: date


class AdoptedDogCreate(AdoptedDogBase):
    owner_id: int


class AdoptedDogUpdate(AdoptionDogBase):
    pass


class AdoptedDogResponse(BaseModel):
    id: int
    id_chip: Optional[int]
    name: str
    about: Optional[str]
    age: int
    is_vaccinated: bool
    image: Optional[str]
    gender: Gender
    entry_date: Optional[date]
    is_sterilized: bool
    is_dewormed: bool
    operation: Optional[str]
    adopted_date: date
    owner: OwnerResponse

    class Config:
        from_attributes = True
