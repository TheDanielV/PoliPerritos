from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.crud.dog import read_adoption_dog_by_id, create_adopted_dog_without_commit
from app.crud.owner import create_owner_without_commit
from app.crud.token import verify_token, mark_token_as_used
from app.crud.user import update_password
from app.models.domain.dog import AdoptedDog


def reset_password(db: Session, token_value: int, new_password: str):
    is_valid, user_id = verify_token(db, token_value)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Token expirado o invalido")
    # Actualiza la contraseña del usuario
    user = update_password(db, user_id, new_password)
    if not user and not isinstance(user, HTTPException):
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    # Marca el token como usado
    mark_token_as_used(db, token_value)

    # Realiza el commit al final para garantizar atomicidad
    db.commit()
    return {"detail": "Contraseña actualizada exitosamente."}


def create_owner_and_adopted_dog(db: Session, adopted_dog: AdoptedDog):
    create_owner_without_commit(db, adopted_dog.owner)
    dog = create_adopted_dog_without_commit(db, adopted_dog)

    if not dog:
        db.rollback()
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    db.commit()
    return {"detail": "Perro Adoptado."}
