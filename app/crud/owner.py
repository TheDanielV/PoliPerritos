# MecanicaMs/app/crud/dog.py
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.domain.owner import Owner
from app.models.schema.owner import *
from app.services.crypt import encrypt_str_data, decrypt_str_data


def create_owner(db: Session, owner: OwnerCreate):
    db_owner = Owner(
        name=owner.name,
        direction=owner.direction,
        cellphone=owner.cellphone,

    )
    db_owner.crypt_data()
    try:
        db.add(db_owner)
        db.commit()
        db.refresh(db_owner)
        return {"detail": "Ya creado"}
    except IntegrityError as ie:
        db.rollback()
        return {"detail": ie}


def create_owner_without_commit(db: Session, owner: Owner):
    owner.crypt_data()
    db.add(owner)


def read_owner_by_id(db: Session, owner_id: int):
    """
    Devuelve un perro estatico por su id.
    """
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    owner.decrypt_data()
    return owner


def update_owner_by_id(db: Session, owner: OwnerCreate, owner_id: int):
    db_owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if owner:
        db_owner.decrypt_data()
        if owner.name and owner.name != db_owner.name:
            db_owner.name = owner.name
        if owner.cellphone and owner.cellphone != db_owner.cellphone:
            db_owner.cellphone = owner.cellphone
        if owner.direction and owner.direction != db_owner.direction:
            db_owner.direction = owner.direction
        db_owner.crypt_data()
    else:
        return HTTPException(status_code=404, detail="Dueño no encontrado")
    try:
        db.merge(db_owner)
        db.commit()
        return {"detail": "Dueño actualizado actualizado"}
    except IntegrityError as ie:
        db.rollback()
        print(ie)
        return HTTPException(status_code=403, detail="could not update")
