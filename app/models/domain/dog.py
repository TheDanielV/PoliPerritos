# app/models/domain/dog.py
from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Enum as SQLAEnum
from sqlalchemy.dialects.mysql import LONGBLOB
from sqlalchemy.orm import relationship
from app.models.schema.owner import OwnerCreate
from app.models.domain.owner import Owner
from app.db.database import Base


# Enumeración para el sexo
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class Dog(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    about = Column(String(255), nullable=True)
    age = Column(Integer, nullable=False)
    is_vaccinated = Column(Boolean, unique=False, nullable=False)
    image = Column(LONGBLOB, nullable=True)
    gender = Column(SQLAEnum(Gender), default=False, nullable=False)


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
            gender=self.gender,
            adopted_date=date,
            owner=owner,
            image=self.image

        )
        return adopted_dog


class AdoptedDog(Dog):
    __tablename__ = "adopted_dogs"

    adopted_date = Column(Date, index=True)
    owner_id = Column(Integer, ForeignKey('owner.id'))
    owner = relationship("Owner", back_populates="adopted_dogs")  # Relacion con Dueño
    visits = relationship('Visit', back_populates='adopted_dog', cascade='all, delete-orphan')  # Relación con Visit

    def unadopt(self):
        adoption_dog = AdoptionDog(
            id=self.id,
            name=self.name,
            about=self.about,
            age=self.age,
            gender=self.gender,
            is_vaccinated=self.is_vaccinated,
            image=self.image
        )
        return adoption_dog
