# MecanicaMs/app/crud/dog.py
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.domain.owner import Owner
from app.models.schema.owner import *


def create_owner(db: Session, owner: OwnerCreate):
    db_owner = Owner(
        name=owner.name,
        direction=owner.direction,
        cellphone=owner.cellphone,

    )
    try:
        db.add(db_owner)
        db.commit()
        db.refresh(db_owner)
        return {"detail": "Ya creado"}
    except IntegrityError as ie:
        db.rollback()
        return {"detail": ie}


def create_owner_without_commit(db: Session, owner: Owner):
    db.add(owner)


def read_owner_by_id(db: Session, owner_id: int):
    """
    Devuelve un perro estatico por id.
    """
    return db.query(Owner).filter(Owner.id == owner_id).first()
