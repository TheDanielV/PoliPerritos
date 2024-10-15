# MecanicaMs/app/crud/dog.py
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.domain.dog import StaticDog
from app.models.schema.dog import *


def create_adopted_dog(db: Session, dog: AdoptedDogCreate):
    db_dog = StaticDog(
        name=dog.name,
        age=dog.age,
        about=dog.about,
        adopted_date=dog.adopted_date
    )
    try:
        db.add(db_dog)
        db.commit()
        db.refresh(db_dog)
        # TODO: agregar el mensaje
        return {"detail": "Vehiculo creado"}
    except IntegrityError as ie:
        db.rollback()
        return {"detail": ie}


def get_dog_by_owner(db: Session, owner_id: str):
    # TODO: Funcion encargada deobtener a el perro por su dueño
    return None  # db.query(Dog).filter(Vehicle.usuario_id == usuario_id).all()



