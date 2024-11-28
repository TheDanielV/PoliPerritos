from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.domain.user import User
from app.services.crypt import get_password_hash


def get_user_id_by_email(db: Session, user_email: str):
    """
    Devuelve el id de un usuario con base en su email.
    """
    user = db.query(User).filter(User.email == user_email).first()
    if user:
        return user.id
    else:
        return None


def get_user_id_by_id(db: Session, user_id: int):
    """
        Devuelve el id de un usuario con base en su email.
    """
    return db.query(User).filter(User.id == user_id).first()


def update_password(db: Session, user_id: int, new_password: str):
    user = get_user_id_by_id(db, user_id)

    if user:
        user.hashed_password = get_password_hash(new_password)
        db.add(user)
        return user
