# app/models/schema/owner.py
from typing import Optional

from pydantic import BaseModel


class OwnerBase(BaseModel):
    name: str
    direction: str
    cellphone: str


class OwnerCreate(OwnerBase):
    pass


class OwnerUpdate(BaseModel):
    name: Optional[str]
    direction: Optional[str]
    cellphone: Optional[str]


class OwnerSecureResponse(BaseModel):
    id: int
    name: str


class OwnerResponse(OwnerBase):
    id: int

    class Config:
        from_attributes = True
