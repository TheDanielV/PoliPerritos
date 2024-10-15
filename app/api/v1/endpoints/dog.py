from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.dog import *
from app.db.session import get_db

router = APIRouter()


@router.post('/', response_model=dict)
def create_new_adopted_dog(dog: AdoptedDogCreate, db: Session = Depends(get_db)):
    result = create_adopted_dog(db, dog)
    if result is None:
        raise HTTPException(status_code=404, detail="Ya existe")
    return result
