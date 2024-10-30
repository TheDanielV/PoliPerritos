# app/models/domain/dog.py
from abc import ABC, abstractclassmethod
from xmlrpc.client import Boolean

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, LargeBinary
from sqlalchemy.orm import relationship
from app.models.schema.owner import OwnerCreate
from app.models.domain.owner import Owner
from app.db.database import Base


# Se crea el modelo paara un usuario
class Dog(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    about = Column(String(255), index=True, nullable=False)
    age = Column(Integer, nullable=False)
    is_vaccinated = Column(Boolean, unique=False)
    image_data = Column(LargeBinary, nullable=True)
    image_type = Column(String(255), nullable=True)


class StaticDog(Dog):
    __tablename__ = "static_dogs"


class AdoptionDog(Dog):
    __tablename__ = "adoption_dogs"

    def adopt(self, date: Date, owner_create: OwnerCreate):
        owner = Owner(
            name=owner_create.name,
            direction=owner_create.direction,
            cellphone=owner_create.cellphone
        )
        adopted_dog = AdoptedDog(
            id=self.id,
            name=self.name,
            about=self.about,
            age=self.age,
            is_vaccinated=self.is_vaccinated,
            adopted_date=date,
            owner=owner

        )
        return adopted_dog


class AdoptedDog(Dog):
    __tablename__ = "adopted_dogs"

    adopted_date = Column(Date, index=True)
    owner_id = Column(Integer, ForeignKey('owner.id'))
    owner = relationship("Owner", back_populates="adopted_dogs")

    def unadopt(self):
        adoption_dog = AdoptionDog(
            id=self.id,
            name=self.name,
            about=self.about,
            age=self.age,
            is_vaccinated=self.is_vaccinated
        )
        return adoption_dog
