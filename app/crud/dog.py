# MecanicaMs/app/crud/dog.py
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.domain.dog import *
from app.models.schema.dog import *
from app.crud.owner import get_owner_by_id


# Crud 4 Static Dogs
def create_static_dog(db: Session, static_dog: StaticDogCreate):
    db_static_dog = StaticDog(
        id=static_dog.id,
        name=static_dog.name,
        about=static_dog.about,
        age=static_dog.age,
        is_vaccinated=static_dog.is_vaccinated
    )
    try:
        db.add(db_static_dog)
        db.commit()
        db.refresh(db_static_dog)
        return {"detail": "Perro Prmanente creado"}
    except IntegrityError as ie:
        db.rollback()
        return None


def get_all_static_dogs(db: Session):
    """
    Devuelve una lista de todos los perros estáticos en la base de datos.
    """
    return db.query(StaticDog).all()


def get_static_dogs_by_id(db: Session, dog_id: int):
    """
    Devuelve un perro estatico por id.
    """
    return db.query(StaticDog).filter(StaticDog.id == dog_id).first()


def delete_an_static_dog_by_id(db: Session, dog_id: int):
    """
    Elimina un perro estatico por id.
    """
    dog = db.query(StaticDog).filter(StaticDog.id == dog_id).first()
    if dog is None:
        return False
    else:
        try:
            db.delete(dog)
            db.commit()
        except IntegrityError:
            db.rollback()  # Deshacer los cambios en caso de error
            return False
        return True


# Crud 4 adoption Dogs
def create_adoption_dog(db: Session, adoption_dog: AdoptionDogCreate):
    db_adoption_dog = AdoptionDog(
        id=adoption_dog.id,
        name=adoption_dog.name,
        about=adoption_dog.about,
        age=adoption_dog.age,
        is_vaccinated=adoption_dog.is_vaccinated
    )
    try:
        db.add(db_adoption_dog)
        db.commit()
        db.refresh(db_adoption_dog)
        return {"detail": "Perro de adopcion creado"}
    except IntegrityError as ie:
        db.rollback()
        return None


def get_all_adoption_dogs(db: Session):
    """
    Devuelve una lista de todos los perros para adopcion en la base de datos.
    """
    return db.query(AdoptionDog).all()


def get_adoption_dog_by_id(db: Session, dog_id: int):
    """
    Devuelve un perro de adopcion por id.
    """
    return db.query(AdoptionDog).filter(AdoptionDog.id == dog_id).first()


def delete_an_adoption_dog_by_id(db: Session, dog_id: int):
    # Obtener el objeto a eliminar
    dog = db.query(AdoptionDog).filter(AdoptionDog.id == dog_id).first()
    if dog is None:
        return False
    else:
        try:
            db.delete(dog)
            db.commit()
        except IntegrityError:
            db.rollback()  # Deshacer los cambios en caso de error
            return False
        return True


def adopt_dog(db: Session, adopted_dog: AdoptedDog):
    adoption_dog = get_adoption_dog_by_id(db, adopted_dog.id)
    try:
        db.add(adopted_dog)
        db.add(adopted_dog.owner)
        db.delete(adoption_dog)
        db.commit()
        db.refresh(adopted_dog)
        db.refresh(adopted_dog.owner)
        return {"detail": "Perro Adoptado creado"}
    except IntegrityError as ie:
        db.rollback()
        return None


def get_all_adopted_dogs(db: Session):
    """
    Devuelve una lista de todos los perros adoptados en la base de datos.
    """
    return db.query(AdoptedDog).all()


def get_adopted_dogs_by_id(db: Session, dog_id: int):
    """
    Devuelve un perro adoptado por id.
    """
    return db.query(AdoptedDog).filter(AdoptedDog.id == dog_id).first()


def unadopt_dog(db: Session, adoption_dog: AdoptionDog, owner_id: int):
    owner = get_owner_by_id(db, owner_id)
    try:
        db.add(adoption_dog)
        db.delete(owner)
        db.commit()
        db.refresh(adoption_dog)
        return {"detail": "Perro des adoptado"}
    except IntegrityError as ie:
        db.rollback()
        return None
