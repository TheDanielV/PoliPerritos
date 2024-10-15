# app/models/schema/dog.py
from datetime import date

from pydantic import BaseModel


# Schema for Abstract Dog
class DogBase(BaseModel):
    name: str
    about: str
    age: int


class DogCreate(DogBase):
    pass


class DogResponse(DogBase):
    id: int

    class Config:
        orm_mode = True


# Schema for Static Dogs
class StaticDogBase(DogBase):
    adopted_date: date


class StaticDogCreate(StaticDogBase):

class StaticDogResponse(StaticDogBase):
    id: int


    class Config:
        orm_mode = True

# Schema for Adoption Dogs
class AdoptionDogBase(DogBase):
    adopted_date: date


class AdoptionDogCreate(AdoptionDogBase):




class AdoptionDogResponse(AdoptionDogBase):
    id: int

    class Config:
        orm_mode = True


# Schema for adopted dogs
class AdoptedDogBase(DogBase):
    adopted_date: date


class AdoptedDogCreate(AdoptedDogBase):
    owner_id: int


class AdoptedDogResponse(AdoptedDogBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
