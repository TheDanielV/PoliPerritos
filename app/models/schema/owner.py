# app/models/schema/owner.py

from pydantic import BaseModel


class OwnerBase(BaseModel):
    name: str
    direction: str
    cellphone: str


class OwnerCreate(OwnerBase):
    pass


class OwnerResponse(OwnerBase):
    id: int

    class Config:
        from_attributes = True
