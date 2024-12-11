from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.owner import create_owner, update_owner_by_id
from app.db.session import get_db
from app.models.domain.user import Role
from app.models.schema.owner import OwnerCreate, OwnerUpdate
from app.models.schema.user import TokenData

router = APIRouter()


@router.put('/update/{id_owner}', response_model=dict)
def update_owner(id_owner: int,
                 owner: OwnerUpdate,
                 db: Session = Depends(get_db),
                 current_user: TokenData = Depends(get_current_user)):
    if current_user.role.value not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    response = update_owner_by_id(db, owner, id_owner)
    return response

