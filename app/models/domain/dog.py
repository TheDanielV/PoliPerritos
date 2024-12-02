# app/models/domain/dog.py
from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Enum as SQLAEnum, Text
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
    id_chip = Column(Integer, index=True, nullable=True)
    name = Column(String(255), nullable=False)
    about = Column(Text, nullable=True)
    age = Column(Integer, nullable=False)
    is_vaccinated = Column(Boolean, unique=False, nullable=False)
    image = Column(LONGBLOB, nullable=True)
    gender = Column(SQLAEnum(Gender), default=False, nullable=False)
    entry_date = Column(Date,nullable=True)
    is_sterilized = Column(Boolean, unique=False, nullable=False)
    is_dewormed = Column(Boolean, unique=False, nullable=False)
    operation = Column(String(255), nullable=True)


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
            id_chip=self.id_chip,
            name=self.name,
            about=self.about,
            age=self.age,
            is_vaccinated=self.is_vaccinated,
            gender=self.gender,
            adopted_date=date,
            owner=owner,
            image=self.image,
            entry_date=self.entry_date,
            is_sterilized=self.is_sterilized,
            is_dewormed=self.is_dewormed,
            operation=self.operation

        )
        return adopted_dog


class AdoptedDog(Dog):
    __tablename__ = "adopted_dogs"

    adopted_date = Column(Date, nullable=False)
    owner_id = Column(Integer, ForeignKey('owner.id'))
    owner = relationship("Owner", back_populates="adopted_dogs")  # Relacion con Dueño
    visits = relationship('Visit', back_populates='adopted_dog', cascade='all, delete-orphan')  # Relación con Visit

    def unadopt(self):
        adoption_dog = AdoptionDog(
            id=self.id,
            id_chip=self.id_chip,
            name=self.name,
            about=self.about,
            age=self.age,
            gender=self.gender,
            is_vaccinated=self.is_vaccinated,
            image=self.image,
            entry_date=self.entry_date,
            is_sterilized=self.is_sterilized,
            is_dewormed=self.is_dewormed,
            operation=self.operation
        )
        return adoption_dog


