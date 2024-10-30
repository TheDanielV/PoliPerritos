# app/models/schema/dog.py
from datetime import date

from pydantic import BaseModel
from app.models.schema.owner import OwnerBase


# Schema for Abstract Dog
class DogBase(BaseModel):
    id: int
    name: str
    about: str
    age: int
    is_vaccinated: bool


class DogCreate(DogBase):
    image_data: bytes = None  # La imagen como bytes opcional
    image_type: str = None  # El tipo de imagen


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


class AdoptedDogResponse(AdoptedDogBase):
    owner_id: int

    class Config:
        orm_mode = True
