from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.owner import *
from app.db.session import get_db

router = APIRouter()


@router.post('/', response_model=dict)
def create_new_owner(owner: OwnerCreate, db: Session = Depends(get_db)):
    result = create_owner(db, owner)
    if result is None:
        raise HTTPException(status_code=404, detail="Ya existe")
    return result
