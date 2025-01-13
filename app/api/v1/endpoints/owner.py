from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.owner import update_owner_by_id, get_all_owners
from app.db.session import get_db
from app.models.domain.user import Role
from app.models.schema.owner import OwnerUpdate, OwnerSecureResponse
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


@router.get('/all/', response_model=List[OwnerSecureResponse])
async def get_owners(db: Session = Depends(get_db),
                     current_user: TokenData = Depends(get_current_user)):
    """
    English:
    --------
    Get all visits.

    Español:
    --------
    Lee todas las visitas.

    """
    if current_user.role.value not in [Role.ADMIN, Role.AUXILIAR]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    owners = get_all_owners(db)
    if not owners:
        raise HTTPException(status_code=404, detail="No hay visitas")
    return owners

