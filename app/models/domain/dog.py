# app/models/domain/dog.py
from abc import ABC, abstractclassmethod

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.database import Base


# Se crea el modelo paara un usuario
class Dog(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    about = Column(String(255), index=True, nullable=False)
    age = Column(Integer, nullable=False)


class StaticDog(Dog):
    __tablename__ = "static_dogs"


class AdoptionDog(Dog):
    __tablename__ = "adoption_dogs"


class AdoptedDog(Dog):
    __tablename__ = "adopted_dogs"

    adopted_date = Column(Date, index=True)
    owner_id = Column(Integer, ForeignKey('owner.id'))
    owner = relationship("Owner", back_populates="adopted_dogs")
